import os
import pybedtools
from seqdataloader.labelgen import *

sc_tasks = '/mnt/lab_data3/soumyak/adpd/deeplearning/sc.tasks.tsv'

sc_params={
    'task_list':sc_tasks,
    'outf':"/mnt/lab_data3/soumyak/adpd/deeplearning/inputs/microglia.input.hdf5",
    'output_type':'hdf5',
    'chrom_sizes':'/users/soumyak/seqdataloader/examples/hg38.chrom.sizes',
    'bin_stride':50,
    'left_flank':400,
    'right_flank':400,
    'bin_size':200,
    'task_threads':1,
    'chrom_threads':20,
    'labeling_approach':'all_genome_bins_regression',
    'store_positives_only':False,
    'allow_ambiguous':False,
    }

genomewide_labels(sc_params)
