from __future__ import division, print_function, absolute_import
import argparse
from pybedtools import BedTool
import pyBigWig 
import pandas as pd
import numpy as np 
import pdb
import csv
import sys
from .classification_label_protocols import *
from .regression_label_protocols import * 
import gzip 
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
#Approaches to determining classification labels
#Others can be added here (imported from classification_label_protocols) 
labeling_approaches={
    "peak_summit_in_bin_classification":peak_summit_in_bin_classification,
    "peak_percent_overlap_with_bin_classification":peak_percent_overlap_with_bin_classification,
    "peak_summit_in_bin_regression":peak_summit_in_bin_regression,
    "peak_percent_overlap_with_bin_regression":peak_percent_overlap_with_bin_regression,
    "all_genome_bins_regression":all_genome_bins_regression
    }

def parse_args():
    parser=argparse.ArgumentParser(description="Generate genome-wide labeled bins for a set of narrowPeak task files ")
    parser.add_argument("--task_list",help="this is a tab-separated file with the name of the task in the first column, the path to the corresponding narrowPeak(.gz) file in the second column (optionally), and the path to the corresponding bigWig file in the third column (optionally, for regression)")
    parser.add_argument("--subset_tasks", nargs='+', default=None)
    parser.add_argument("--task_list_sep",default='\t')
    parser.add_argument("--outf",help="output filename that labeled bed file will be saved to.")
    parser.add_argument("--output_type",choices=['gzip','hdf5','pkl','bz2'],default='gzip',help="format to save output, one of gzip, hdf5, pkl, bz2")
    parser.add_argument("--split_output_by_chrom",action="store_true",default=False)
    parser.add_argument("--split_output_by_task",action="store_true",default=False,help="creates a separate output file for each task's labels")
    parser.add_argument("--chrom_sizes",help="chromsizes file for the reference genome. First column is chrom name; second column is chrom size")
    parser.add_argument("--chroms_to_keep",nargs="+",default=None,help="list of chromosomes, as defined in the --chrom_sizes file, to include in label generation. All chromosomes will be used if this argument is not provided. This is most useful if generating a train/test/validate split for deep learning models")
    parser.add_argument("--chroms_to_exclude",nargs="+",default=None,help="list of chromosomes, as defined in the --chrom_sizes file, to exclude in label generation. No chromosomes will be excluded if this argument is not provided. This is most useful if generating a train/test/validate split for deep learning models")
    parser.add_argument("--bin_stride",type=int,default=50,help="bin_stride to shift adjacent bins by")
    parser.add_argument("--left_flank",type=int,default=400,help="left flank")
    parser.add_argument("--right_flank",type=int,default=400,help="right flank")
    parser.add_argument("--bin_size",type=int,default=200,help="flank around bin center where peak summit falls in a positive bin")

    parser.add_argument("--task_threads",type=int,default=1,help="Number of tasks to process for a given chromosome.")
    parser.add_argument("--chrom_threads",type=int,default=4,help="Number of chromosomes to process at once.")
    parser.add_argument("--bigwig_stats",choices=['mean','min','max','coverage','std'],default='mean',help="Value to extract from bigwig file")
    parser.add_argument("--overlap_thresh",type=float,default=0.5,help="minimum percent of bin that must overlap a peak for a positive label")
    parser.add_argument("--allow_ambiguous",default=False,action="store_true")
    parser.add_argument("--store_positives_only",default=False,action="store_true")
    parser.add_argument("--store_values_above_thresh",default=None,type=float,help="for the regression case, determine the minimum row value to include in the output data frame (i.,e. remove bins that are 0 for all tasks by setting this to 0") 
    parser.add_argument("--labeling_approach",choices=["peak_summit_in_bin_classification",
                                                       "peak_percent_overlap_with_bin_classification",
                                                       "peak_summit_in_bin_regression",
                                                       "peak_percent_overlap_with_bin_regression",
                                                       "all_genome_bins_regression"])
    parser.add_argument("--label_transformer",default="asinh",help="type of transformation to apply to the labels; one of None, asinh, log10, log")
    parser.add_argument("--label_transformer_pseudocount",type=float,default=0.001,help="pseudocount to add to values if using log10 or log label transformations")
    
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)       
    return parser.parse_args()

def get_labels_one_task(inputs):
    #unravel the inputs 
    task_name=inputs[0]
    task_bed=inputs[1]
    task_bigwig=inputs[2]
    task_ambig=inputs[3]
    chrom=inputs[4]
    first_coord=inputs[5]
    final_coord=inputs[6]
    args=inputs[7]
    #determine the appropriate labeling approach
    print("in get_labels_one_task") 
    return labeling_approaches[args.labeling_approach](task_name,task_bed,task_bigwig,task_ambig,chrom,first_coord,final_coord,args)    
    
def get_chrom_labels(inputs):

    #unravel inputs 
    chrom=inputs[0]
    chrom_size=inputs[1]
    bed_and_bigwig_dict=inputs[2]
    tasks=inputs[3]
    args=inputs[4] 

    #pre-allocate a pandas data frame to store bin labels for the current chromosome. Fill with zeros    
    #determine the index tuple values
    try:
        chroms,all_start_pos,all_end_pos,first_bin_start,final_bin_start=get_indices(chrom,chrom_size,args)
    except:
        return (chrom,None)
    columns=['CHR','START','END']+list(tasks[0])
    num_entries=len(chroms.values)
    chrom_df = pd.DataFrame(0,index=np.arange(num_entries),columns=columns)
    chrom_df['CHR']=chroms.values
    chrom_df['START']=all_start_pos.values
    chrom_df['END']=all_end_pos.values 
    
    print("pre-allocated df for chrom:"+str(chrom)+"with dimensions:"+str(chrom_df.shape))

    #create a thread pool to label bins, each task gets assigned a thread 
    pool_inputs=[]
    for task_name in bed_and_bigwig_dict:
        task_bed=bed_and_bigwig_dict[task_name]['bed']
        task_bigwig=bed_and_bigwig_dict[task_name]['bigwig']
        task_ambig=bed_and_bigwig_dict[task_name]['ambig'] 
        pool_inputs.append((task_name,task_bed,task_bigwig,task_ambig,chrom,first_bin_start,final_bin_start,args))

    with ProcessPoolExecutor(max_workers=args.task_threads) as pool: 
        bin_values=pool.map(get_labels_one_task,pool_inputs)
    
    for task_name,task_labels in bin_values:
        if task_labels is None:
            continue
        chrom_df[task_name]=task_labels
    if args.split_output_by_chrom==True:
        assert args.output_type in ["gzip","bz2"]
        index_label=['Chrom','Start','End']
        chrom_df.to_csv(args.outf+"."+chrom,sep='\t',float_format="%.2f",header=True,index=True,index_label=index_label,mode='wb',compression=args.output_type,chunksize=1000000) 
    return (chrom, chrom_df)

def get_bed_and_bigwig_dict(tasks):
    print("creating dictionary of bed files and bigwig files for each task:")
    bed_and_bigwig_dict=dict()
    for index,row in tasks.iterrows():
        task_name=row[0]
        print(task_name) 
        bed_and_bigwig_dict[task_name]=dict()
        
        #get the peak file associated with the task (if provided)
        if pd.isna(row[1]):
            task_bed=None
        else:
            assert os.path.exists(row[1])
            try:
                task_bed=BedTool(row[1])
            except:
                raise Exception("Could not parse:"+str(row[1]))
        bed_and_bigwig_dict[task_name]['bed']=task_bed
        
        #get the BigWig file associated with the task (if provided)
        if pd.isna(row[2]):
            task_bigwig=None
        else:
            assert os.path.exists(row[2])
            try:
                task_bigwig=pyBigWig.open(row[2])
            except:
                raise Exception("Could not parse:"+str(row[2]))
        bed_and_bigwig_dict[task_name]['bigwig']=row[2] #need to parse the pyBigWig inside Pool
        
        #get the ambiguous peaks
        if pd.isna(row[3]):
            ambig_bed=None
        else: 
            assert os.path.exists(row[3])
            try:
                ambig_bed=BedTool(row[3])
            except:
                raise Exception("Could not parse:"+str(row[3]))
        bed_and_bigwig_dict[task_name]['ambig']=ambig_bed
        
    return bed_and_bigwig_dict

def get_indices(chrom,chrom_size,args):
    final_bin_start=((chrom_size-args.right_flank-args.bin_size)//args.bin_stride)*args.bin_stride
    #final_coord=(chrom_size//args.bin_stride)*args.bin_stride
    first_bin_start=args.left_flank
    if final_bin_start<=first_bin_start:
        print("the chromosome"+chrom+" is too short for the specified settings of --left_flank, --right_flank, --bin_size, skipping")
        return None 
    chroms=[]
    start_pos=[]
    end_pos=[]
    for index in range(first_bin_start,final_bin_start+1,args.bin_stride):
        chroms.append(chrom)
        start_pos.append(index-args.left_flank)
        end_pos.append(index+args.bin_size+args.right_flank)
    return pd.Series(chroms),pd.Series(start_pos),pd.Series(end_pos),first_bin_start,final_bin_start 


def write_output(task_names,full_df,first_chrom,args,mode='w',task_split_engaged=False,outf=None):
    '''
    Save genome-wide labels to disk in gzip, hdf5, or pkl format 
    '''
    if (args.split_output_by_task==True) and (task_split_engaged==False) :
        for task in task_names:
            task_df=full_df[['CHR','START','END',task]]
            write_output([task],task_df,first_chrom,args,mode=mode,task_split_engaged=True,outf=task.replace('/','.')+"."+args.outf)
        return
    if outf==None:
        outf=args.outf        
    all_negative_df=None
    if args.store_positives_only==True:
        #find regions with at least one positive entry per task
        all_negative_df=full_df[['CHR','START','END']][(full_df[task_names]<=0).all(1)]
        full_df=full_df[(full_df[task_names]>0).any(1)]
    if args.store_values_above_thresh is not None:
        all_negative_df=full_df[['CHR','START','END']][(full_df[task_names]<=args.store_values_above_thresh).all(1)]
        full_df=full_df[(full_df[task_names]>args.store_values_above_thresh).any(1)]
        
    #determine if header needs to be stored
    if first_chrom is True:
        header=True
    else:
        header=False
    if args.output_type=="gzip":
        full_df.to_csv(outf,sep='\t',header=header,index=False,mode=mode+'b',compression='gzip',chunksize=1000000)
        if all_negative_df is not None:
            all_negative_df.to_csv("universal_negatives."+outf,sep='\t',header=header,index=False,mode=mode+'b',compression='gzip',chunksize=1000000)
    elif args.output_type=="bz2":
        full_df.to_csv(outf,sep='\t',header=header,index=False,mode=mode+'b',compression='bz2',chunksize=1000000)
        if all_negative_df is not None:
            all_negative_df.to_csv("universal_negatives."+outf,sep='\t',header=header,index=False,mode=mode+'b',compression='bz2',chunksize=1000000)
    elif args.output_type=="hdf5":
        full_df=full_df.set_index(['CHR','START','END'])
        if mode=='w':
            append=False
        else:
            append=True
        full_df.to_hdf(outf,key="data",mode=mode, append=append, format='table',min_itemsize={'CHR':30})
        if all_negative_df is not None:
            all_negative_df.set_index(['CHR','START','END'])
            all_negative_df.to_hdf("universal_negatives."+outf,key="data",mode=mode, append=append, format='table',min_itemsize={'CHR':30})
    elif args.output_type=="pkl":
        full_df=full_df.set_index(['CHR','START','END'])        
        full_df.to_pickle(outf,compression="gzip")
        if all_negative_df is not None:
            all_negative_df.set_index(['CHR','START','END'])
            all_negative_df.to_pickle("universal_negatives."+outf,compression="gzip")

def args_object_from_args_dict(args_dict):
    #create an argparse.Namespace from the dictionary of inputs
    args_object=argparse.Namespace()
    #set the defaults
    vars(args_object)['split_output_by_chrom']=False
    vars(args_object)['split_output_by_task']=False
    vars(args_object)['chroms_to_keep']=None
    vars(args_object)['chroms_to_exclude']=None
    vars(args_object)['bin_stride']=50
    vars(args_object)['left_flank']=400
    vars(args_object)['right_flank']=400
    vars(args_object)['bin_size']=200
    vars(args_object)['chrom_threads']=4
    vars(args_object)['task_threads']=1
    vars(args_object)['overlap_thresh']=0.5
    vars(args_object)['allow_ambiguous']=True
    vars(args_object)['store_positives_only']=False
    vars(args_object)['store_values_above_thresh']=None
    vars(args_object)['output_hdf5_low_mem']=False
    vars(args_object)['task_list_sep']='\t'
    vars(args_object)['bigwig_stats']='mean'
    vars(args_object)['label_transformer']='asinh'
    vars(args_object)['label_transformer_pseudocount']=0.001 
    for key in args_dict:
        vars(args_object)[key]=args_dict[key]
    #set any defaults that are unset 
    args=args_object    
    return args 
        
def genomewide_labels(args):
    if type(args)==type({}):
        args=args_object_from_args_dict(args)
        
    #read in the metadata file with:
    #task names in column 1,
    #path to peak file in column 2,
    #path to bigWig file in column 3
    #path to ambiguous peaks in column 4 (bed) 
    tasks=pd.read_csv(args.task_list,sep=args.task_list_sep,header=None)
    if args.subset_tasks != None:
        tasks = tasks[tasks[0].isin(args.subset_tasks)]
    print(tasks)
    bed_and_bigwig_dict=get_bed_and_bigwig_dict(tasks) 

    #col1: chrom name
    #col2: chrom size 
    chrom_sizes=pd.read_csv(args.chrom_sizes,sep='\t',header=None)

    processed_first_chrom=False
    #create a Pool to process chromosomes in parallel
    pool_args=[]
    chrom_order=[] 
    for index,row in chrom_sizes.iterrows():
        chrom=row[0]
        
        #determine whether this chromosome should be included in the label file
        if args.chroms_to_keep!=None:
            if chrom not in args.chroms_to_keep:
                continue
        if args.chroms_to_exclude!=None:
            if chrom in args.chroms_to_exclude:
                continue 
        chrom_order.append(chrom) 
        chrom_size=row[1]
        pool_args.append((chrom,chrom_size,bed_and_bigwig_dict,tasks,args))
    print("creating chromosome thread pool")
    with ProcessPoolExecutor(max_workers=args.chrom_threads) as pool: 
        processed_chrom_outputs=pool.map(get_chrom_labels,pool_args)

    #if the user is happy with separate files for each chromosome, these have already been written to disk. We are done 
    if args.split_output_by_chrom==True:
        exit()
    mode='w'
    first_chrom=True
    for chrom, chrom_df in processed_chrom_outputs:
        #write to output file!
        if chrom_df is None:
            continue 
        print("writing output chromosomes:"+str(chrom))
        write_output(tasks[0],chrom_df,first_chrom,args,mode=mode)
        first_chrom=False
        mode='a'
    print("done!")
    
def main():
    args=parse_args()     
    genomewide_labels(args)
    
if __name__=="__main__":
    #try:
    #    multiprocessing.set_start_method('spawn')
    #except:
    #    print("context already set") 
    main()
