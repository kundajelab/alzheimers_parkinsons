from math import floor,ceil
import pandas as pd
from .utils import rolling_window 
import pdb
import numpy as np 
from pybedtools import BedTool
import pyBigWig

def transform_label_vals(labels,label_transformer,pseudocount=0.001):
    if label_transformer is None:
        return labels
    elif label_transformer=="None":
        return labels 
    elif label_transformer == 'asinh':
        return np.arcsinh(labels)
    elif label_transformer == 'log10':
        return np.log10(labels+pseudocount)
    elif label_transformer == 'log':
        return np.log(labels+pseudocount)
    else:
        raise Exception("transform_label_vals argument must be one of None, asinh, log10, log; you provided:"+str(label_transformer)) 


def peak_summit_in_bin_regression(task_name,task_bed,task_bigwig,task_ambig,chrom,first_bin_start,final_bin_start,args):
    '''
    For each peak, the summit position is determined. 

    The minimum bin with bedtools coverage is args.binsize upstream of the summit;
    The max bin with bedtools coverage is args.binsize downstream of the summit 

    Within this range, bin centers are shifted by args.bin_stride 

    If specified in args.allow_ambiguous, then coverage is also computed in adjacent bins to the two extremes are marked as 
    ambiguous 
    '''
    print("starting chromosome:"+str(chrom)+" for task:"+str(task_name))
    task_bigwig=pyBigWig.open(task_bigwig)
    #get the peaks for the current chromosome by intersecting the task_bed with the chromosome coordinates 
    min_chrom_coord=first_bin_start
    max_chrom_coord=final_bin_start
    if min_chrom_coord >= max_chrom_coord:
        print("the chromosome"+chrom+" is too short for the specified settings of --left_flank, --right_flank, --bin_size, skipping")
        return task_name, None
    chrom_coords=chrom+'\t'+str(min_chrom_coord)+'\t'+str(max_chrom_coord)
    chrom_bed=BedTool(chrom_coords,from_string=True)
    chrom_task_bed=task_bed.intersect(chrom_bed)
    chrom_ambig_bed=None
    if ((args.allow_ambiguous==True) and (task_ambig!=None)):
        chrom_ambig_bed=task_ambig.intersect(chrom_bed)
    print("got peak subset for chrom:"+str(chrom)+" for task:"+str(task_name))
    
    #pre-allocate a numpy array of 0's
    num_bins=(final_bin_start-first_bin_start)//args.bin_stride+1 
    coverage_vals=np.zeros(num_bins)
    for entry in chrom_task_bed:
        chrom=entry[0]
        peak_start=int(entry[1])
        peak_end=int(entry[2])
        summit=peak_start+int(entry[-1])

        chromosome_min_bin_index=ceil((summit-args.bin_size)/args.bin_stride)
        min_bin_start=chromosome_min_bin_index*args.bin_stride
        chromosome_max_bin_index=floor(summit/args.bin_stride)
        max_bin_start=chromosome_max_bin_index*args.bin_stride 

        #if allow_ambiguous supplied by user, shift 1 bin left and 1 bin right 
        if args.allow_ambiguous==True:
            min_bin_start-=args.bin_stride
            chromosome_min_bin_index-=1
            max_bin_start+=args.bin_stride
            chromosome_max_bin_index+=1
            
        #get mean coverage in bigwig for each bin specified above
        index_coverage_vals=chromosome_min_bin_index
        for bin_start in range(min_bin_start,max_bin_start+1,args.bin_stride):
            if index_coverage_vals>=0 and index_coverage_vals < num_bins:
                try:
                    coverage_vals[index_coverage_vals]=task_bigwig.stats(chrom,bin_start,bin_start+args.bin_size,args.bigwig_stats)[0]
                except:
                    print("could not get coverage:"+str(chrom)+":"+str(bin_start)+"-"+str(bin_start+args.bin_size)+" for task:"+str(task_name))
            index_coverage_vals+=1
    print("checking ambig")
    if chrom_ambig_bed!=None:
        for entry in chrom_ambig_bed:
            chrom=entry[0]
            peak_start=int(entry[1])
            peak_end=int(entry[2])
            summit=peak_start+int(entry[-1])

            chromosome_min_bin_index=ceil((summit-args.bin_size)/args.bin_stride)
            min_bin_start=chromosome_min_bin_index*args.bin_stride
            chromosome_max_bin_index=floor(summit/args.bin_stride)
            max_bin_start=chromosome_max_bin_index*args.bin_stride
            
            #get mean coverage in bigwig for each bin specified above
            index_coverage_vals=chromosome_min_bin_index
            for bin_start in range(min_bin_start,max_bin_start+1,args.bin_stride):
                if index_coverage_vals>=0 and index_coverage_vals < num_bins: 
                    coverage_vals[index_coverage_vals]=np.nan
                index_coverage_vals+=1
    print("finished chromosome:"+str(chrom)+" for task:"+str(task_name))
    tranformed_vals=transform_label_vals(coverage_vals,args.label_transformer,args.label_transformer_pseudocount)
    return task_name,transformed_vals

def peak_percent_overlap_with_bin_regression(task_name,task_bed,task_bigwig,task_ambig,chrom,first_bin_start,final_bin_start,args):
    '''
    50% of the central 200bp region in a 1kb bin must overlap with the peak for coverage to be computed in the provided bigWig 
    '''
    #get the peaks for the current chromosome by intersecting the task_bed with the chromosome coordinates
    print("starting chromosome:"+str(chrom)+" for task:"+str(task_name))
    task_bigwig=pyBigWig.open(task_bigwig)
    min_chrom_coord=first_bin_start
    max_chrom_coord=final_bin_start
    if min_chrom_coord >= max_chrom_coord:
        print("the chromosome"+chrom+" is too short for the specified settings of --left_flank, --right_flank, --bin_size, skipping")
        return task_name,None
    chrom_coords=chrom+'\t'+str(min_chrom_coord)+'\t'+str(max_chrom_coord)
    chrom_bed=BedTool(chrom_coords,from_string=True)
    chrom_task_bed=task_bed.intersect(chrom_bed)
    chrom_ambig_bed=None
    if ((args.allow_ambiguous==True) and (task_ambig!=None)):
        chrom_ambig_bed=task_ambig.intersect(chrom_bed)
        
    print("got peak subset for chrom:"+str(chrom)+" for task:"+str(task_name))
    #pre-allocate a numpy array of 0's
    num_bins=(final_bin_start-first_bin_start)//args.bin_stride+1 
    coverage_vals=np.zeros(num_bins)    
    for entry in chrom_task_bed:
        chrom=entry[0]
        peak_start=int(entry[1])
        peak_end=int(entry[2])
        min_overlap=int(round(args.overlap_thresh*args.bin_size))        

        #get the bin indices that overlap the peak
        chromosome_min_bin_index=(peak_start-min_overlap-first_bin_start)//args.bin_stride
        min_bin_start=chromosome_min_bin_index*args.bin_stride 
        chromosome_max_bin_index=(peak_end-min_overlap-first_bin_start)//args.bin_stride
        max_bin_start=chromosome_max_bin_index*args.bin_stride

        #if allow_ambiguous supplied by user, shift 1 bin left and 1 bin right 
        if args.allow_ambiguous==True:
            min_bin_start-=args.bin_stride
            chromosome_min_bin_index-=1
            max_bin_start+=args.bin_stride
            chromosome_max_bin_index+=1

        #get mean coverage in bigwig for each bin specified above 
        index_coverage_vals=chromosome_min_bin_index
        for bin_start in range(min_bin_start,max_bin_start+1,args.bin_stride):
            if index_coverage_vals>=0 and index_coverage_vals < num_bins:
                try:
                    coverage_vals[index_coverage_vals]=task_bigwig.stats(chrom,bin_start,bin_start+args.bin_size,args.bigwig_stats)[0]
                except:
                    print("could not get coverage:"+str(chrom)+":"+str(bin_start)+"-"+str(bin_start+args.bin_size)+" for task:"+str(task_name))
                    
            index_coverage_vals+=1
    if ((args.allow_ambiguous==True) and (task_ambig!=None)):
        for entry in chrom_ambig_bed:
            chrom=entry[0]
            peak_start=int(entry[1])
            peak_end=int(entry[2])
            min_overlap=int(round(args.overlap_thresh*args.bin_size))        

            #get the bin indices that overlap the peak
            chromosome_min_bin_index=(peak_start-min_overlap-first_bin_start)//args.bin_stride
            min_bin_start=chromosome_min_bin_index*args.bin_stride 
            chromosome_max_bin_index=(peak_end-min_overlap-first_bin_start)//args.bin_stride
            max_bin_start=chromosome_max_bin_index*args.bin_stride
            #get mean coverage in bigwig for each bin specified above 
            index_coverage_vals=chromosome_min_bin_index
            for bin_start in range(min_bin_start,max_bin_start+1,args.bin_stride):
                if index_coverage_vals>=0 and index_coverage_vals < num_bins:
                    coverage_vals[index_coverage_vals]=np.nan
                index_coverage_vals+=1        
    print("finished chromosome:"+str(chrom)+" for task:"+str(task_name))
    transformed_vals=transform_label_vals(coverage_vals,args.label_transformer,args.label_transformer_pseudocount)
    return task_name,transformed_vals

def all_genome_bins_regression(task_name,task_bed,task_bigwig,task_ambig,chrom,first_bin_start,final_bin_start,args):
    '''
    compute bigWig coverage for all bins in the chromosome, regardless of whether a called peak overlaps the bin
    '''
    print("starting chromosome:"+str(chrom)+" for task:"+str(task_name))
    task_bigwig=pyBigWig.open(task_bigwig)
    #get the BigWig value at each position along the chromosome, (cutting off anything that extends beyond final_coord)
    try:
        values=task_bigwig.values(chrom,first_bin_start,final_bin_start+args.bin_size,numpy=True)
    except:
        print("Warning! Chromosome:"+str(chrom)+" appears not to be present in the bigWig file for task:"+task_name)
        return task_name,None
    #replace nan values with 0 
    values=np.nan_to_num(values) 
    #reshape the values such that number of columns is equal to the bin_stride 
    values=np.reshape(values,((final_bin_start+args.bin_size-first_bin_start)//args.bin_stride,args.bin_stride))
    #sum across the columns
    strided_sums=np.sum(values,axis=1)

    #compute rolling average for each bin
    bin_means=np.sum(rolling_window(strided_sums,args.bin_size//args.bin_stride),-1)/args.bin_size
    norm_bin_means=transform_label_vals(bin_means,args.label_transformer,args.label_transformer_pseudocount)
    num_bins=norm_bin_means.shape[0]
    #add in ambiguous bins
    chrom_ambig_bed=None
    if ((args.allow_ambiguous==True) and (task_ambig is not None)):
        min_chrom_coord=first_bin_start
        max_chrom_coord=final_bin_start
        if min_chrom_coord >= max_chrom_coord:
            print("the chromosome"+chrom+" is too short for the specified settings of --left_flank, --right_flank, --bin_size, skipping")
            return task_name,None
        chrom_coords=chrom+'\t'+str(min_chrom_coord)+'\t'+str(max_chrom_coord)
        chrom_bed=BedTool(chrom_coords,from_string=True)
        chrom_ambig_bed=task_ambig.intersect(chrom_bed)
        for entry in chrom_ambig_bed:
            chrom=entry[0]
            peak_start=int(entry[1])
            peak_end=int(entry[2])
            summit=peak_start+int(entry[-1])
            chromosome_min_bin_index=ceil((summit-args.bin_size)/args.bin_stride)
            min_bin_start=chromosome_min_bin_index*args.bin_stride
            chromosome_max_bin_index=floor(summit/args.bin_stride)
            max_bin_start=chromosome_max_bin_index*args.bin_stride
            
            #get mean coverage in bigwig for each bin specified above
            index_coverage_vals=chromosome_min_bin_index
            for bin_start in range(min_bin_start,max_bin_start+1,args.bin_stride):
                if index_coverage_vals>=0 and index_coverage_vals < num_bins: 
                    norm_bin_means[index_coverage_vals]=np.nan
                index_coverage_vals+=1        
    print("finished chromosome:"+str(chrom)+" for task:"+str(task_name))
    return task_name,norm_bin_means 

