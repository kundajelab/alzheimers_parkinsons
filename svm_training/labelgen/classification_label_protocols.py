from math import floor,ceil
import pandas as pd
from multiprocessing.pool import ThreadPool
from .utils import rolling_window
import pdb
import numpy as np
from pybedtools import BedTool


def peak_summit_in_bin_classification(task_name,task_bed,task_bigwig,task_ambig,chrom,first_bin_start,final_bin_start,args):
    '''
    For each peak, the summit position is determined.

    The minimum bin with bedtools coverage is args.binsize upstream of the summit;
    The max bin with bedtools coverage is args.binsize downstream of the summit

    Within this range, bin centers are shifted by args.bin_stride

    If specified in args.allow_ambiguous, then coverage is also computed in adjacent bins to the two extremes are marked as
    ambiguous
    '''
    #get the peaks for the current chromosome by intersecting the task_bed with the chromosome coordinates
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
        summit=peak_start+int(entry[-1])

        chromosome_min_bin_index=ceil((summit-args.bin_size-first_bin_start)/args.bin_stride)
        min_bin_start=chromosome_min_bin_index*args.bin_stride
        chromosome_max_bin_index=floor((summit-first_bin_start)/args.bin_stride)
        max_bin_start=chromosome_max_bin_index*args.bin_stride

        #get mean coverage in bigwig for each bin specified above
        index_coverage_vals=chromosome_min_bin_index
        for bin_start in range(min_bin_start,max_bin_start+1,args.bin_stride):
            if index_coverage_vals >= 0 and index_coverage_vals <= (num_bins - 1):
                coverage_vals[index_coverage_vals]=1
            index_coverage_vals+=1

        #if allow_ambiguous supplied by user, shift 1 bin left and 1 bin right
        if args.allow_ambiguous==True:
            chromosome_min_bin_index-=1
            if chromosome_min_bin_index > 0 and chromosome_min_bin_index <= (num_bins - 1):
                coverage_vals[chromosome_min_bin_index]=np.nan
            chromosome_max_bin_index+=1
            if chromosome_max_bin_index >= 0 and chromosome_max_bin_index < (num_bins - 1):
                coverage_vals[chromosome_max_bin_index]=np.nan
                
    #if a bed file of ambiguous labels is specified, label them with -1
    if ((args.allow_ambiguous==True) and (chrom_ambig_bed!=None)):
        for entry in chrom_ambig_bed:
            chrom=entry[0]
            peak_start=int(entry[1])
            peak_end=int(entry[2])
            summit=peak_start+int(entry[-1])

            chromosome_min_bin_index=ceil((summit-args.bin_size-first_bin_start)/args.bin_stride)
            min_bin_start=chromosome_min_bin_index*args.bin_stride
            chromosome_max_bin_index=floor((summit-first_bin_start)/args.bin_stride)
            max_bin_start=chromosome_max_bin_index*args.bin_stride

            #get mean coverage in bigwig for each bin specified above
            index_coverage_vals=chromosome_min_bin_index
            for bin_start in range(min_bin_start,max_bin_start+1,args.bin_stride):
                if index_coverage_vals >= 0 and index_coverage_vals <= (num_bins - 1):
                    coverage_vals[index_coverage_vals]=np.nan
                index_coverage_vals+=1
        
    print("finished chromosome:"+str(chrom)+" for task:"+str(task_name))
    return task_name,coverage_vals

def peak_percent_overlap_with_bin_classification(task_name,task_bed,task_bigwig,task_ambig,chrom,first_bin_start,final_bin_start,args):
    '''
    50% of the central 200bp region in a 1kb bin must overlap with the peak for a positive label
    '''
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
        min_overlap=int(round(args.overlap_thresh*min(args.bin_size, (peak_end-peak_start))))

        #get the bin indices that overlap the peak
        chromosome_min_bin_index=ceil((peak_start-(args.bin_size-min_overlap)-first_bin_start)/args.bin_stride)
        min_bin_start=chromosome_min_bin_index*args.bin_stride
        chromosome_max_bin_index=floor((peak_end-min_overlap-first_bin_start)/args.bin_stride)
        max_bin_start=chromosome_max_bin_index*args.bin_stride

        #get mean coverage in bigwig for each bin specified above
        index_coverage_vals=chromosome_min_bin_index
        for bin_start in range(min_bin_start,max_bin_start+1,args.bin_stride):
            if index_coverage_vals >= 0 and index_coverage_vals <= (num_bins - 1):
                coverage_vals[index_coverage_vals]=1
                index_coverage_vals+=1

        #if allow_ambiguous supplied by user, shift 1 bin left and 1 bin right
        if args.allow_ambiguous==True:
            if chromosome_min_bin_index > 0 and chromosome_min_bin_index <= (num_bins - 1):
                chromosome_min_bin_index-=1
                coverage_vals[chromosome_min_bin_index]=np.nan
            if chromosome_max_bin_index >= 0 and chromosome_max_bin_index < (num_bins - 1):
                chromosome_max_bin_index+=1
                coverage_vals[chromosome_max_bin_index]=np.nan
    if ((args.allow_ambiguous==True) and (task_ambig!=None)):
        for entry in chrom_ambig_bed:
            chrom=entry[0]
            peak_start=int(entry[1])
            peak_end=int(entry[2])
            min_overlap=int(round(args.overlap_thresh*min(args.bin_size, (peak_end-peak_start))))

            #get the bin indices that overlap the peak
            chromosome_min_bin_index=ceil((peak_start-(args.bin_size-min_overlap)-first_bin_start)/args.bin_stride)
            min_bin_start=chromosome_min_bin_index*args.bin_stride
            chromosome_max_bin_index=floor((peak_end-min_overlap-first_bin_start)/args.bin_stride)
            max_bin_start=chromosome_max_bin_index*args.bin_stride

            #get mean coverage in bigwig for each bin specified above
            index_coverage_vals=chromosome_min_bin_index
            for bin_start in range(min_bin_start,max_bin_start+1,args.bin_stride):
                if index_coverage_vals >= 0 and index_coverage_vals <= (num_bins - 1):
                    coverage_vals[index_coverage_vals]=np.nan
                    index_coverage_vals+=1
        
    print("finished chromosome:"+str(chrom)+" for task:"+str(task_name))
    return task_name,coverage_vals
