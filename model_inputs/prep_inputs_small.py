import os
import pybedtools
from seqdataloader.labelgen import *

adpd_tasks = 'tasks.small.tsv'
    
input_params={
    'task_list':adpd_tasks,
    'outf':"small.hdf5",
    'output_type':'hdf5',
    'chrom_sizes':'hg38.chrom.sizes',
    'bin_stride':50,
    'left_flank':400,
    'right_flank':400,
    'bin_size':200,
    'threads':1,
    'subthreads':40,
    'labeling_approach':'peak_summit_in_bin_regression',
    'store_positives_only':True,
    'allow_ambiguous':True,
    }

genomewide_labels(input_params)

