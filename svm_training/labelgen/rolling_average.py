import numpy as np
import pandas as pd 
import pyBigWig
import pandas as pd 
import pdb
from math import floor

def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)
            

task_bigwig=pyBigWig.open("./bigwig_files_from_encode_for_label_comparison/ENCFF842XRQ.bigWig")
chromsizes=pd.read_csv("hg38.chrom.sizes",header=None,sep='\t')
bin_size=200
bin_stride=50
left_flank=400
right_flank=400
seq_size=left_flank+right_flank+bin_size
task_name="test"
for index,row in chromsizes.iterrows():
    chrom=row[0]
    chromsize=row[1]
    nbins=chromsize//bin_stride
    final_coord=nbins*bin_stride 
    print(final_coord)
    print(chromsize) 
    values=task_bigwig.values(chrom,0,final_coord,numpy=True)
    print("got values") 
    cols=bin_stride
    rows=final_coord//cols 
    values=np.reshape(values,(rows,cols))
    print("completed reshape!") 
    #sum the bins
    binsums=np.sum(values,axis=1)
    print("completed bin sums")
    bin_means=np.sum(rolling_window(binsums,bin_size//bin_stride),-1)/bin_size 
    print("rolled")
    non_zero_inds=np.nonzero(bin_means)[0]
    non_zero_seq_start=non_zero_inds*bin_stride-left_flank
    non_zero_seq_end=non_zero_seq_start+seq_size
    non_zero_bins=dict()
    for i in range(non_zero_inds.shape[0]):
        bin_index=non_zero_inds[i]
        cur_bin_mean=bin_means[bin_index]
        non_zero_bins[(chrom,non_zero_seq_start[i],non_zero_seq_end[i])]=dict()
        non_zero_bins[(chrom,non_zero_seq_start[i],non_zero_seq_end[i])][task_name]=cur_bin_mean
    print("finished chrom:"+str(chrom)+" for task:"+str(task_name))                                                                      
    
