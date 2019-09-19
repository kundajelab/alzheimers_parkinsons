import os
import pybedtools
from kerasAC.splits import *
from seqdataloader.labelgen import *
import sys

cluster = int(sys.argv[1])
split = int(sys.argv[2])
sc_tasks = '/users/soumyak/alzheimers_parkinsons/model_inputs/sc.tasks.tsv'
test_chroms = hg19_splits[split]['test']

train_params={
    'task_list':sc_tasks,
    'subset_tasks':['Cluster'+str(cluster)],
    'outf':'/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+str(cluster)+'/fold'+str(split)+'/train/train.inputs.bed.gz',
    'output_type':'gzip',
    'chrom_sizes':'/users/soumyak/seqdataloader/examples/hg38.chrom.sizes',
    'bin_stride':50,
    'left_flank':400,
    'right_flank':400,
    'bin_size':200,
    'task_threads':1,
    'chrom_to_exclude':test_chroms,
    'chrom_threads':1,
    'labeling_approach':'peak_summit_in_bin_classification',
    'store_positives_only':False,
    'allow_ambiguous':True,
    }

test_params={
    'task_list':sc_tasks,
    'subset_tasks':['Cluster'+str(cluster)],
    'outf':'/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+str(cluster)+'/fold'+str(split)+'/test/test.inputs.bed.gz',
    'output_type':'gzip',
    'chrom_sizes':'/users/soumyak/seqdataloader/examples/hg38.chrom.sizes',
    'bin_stride':50,
    'left_flank':400,
    'right_flank':400,
    'bin_size':200,
    'task_threads':1,
    'chrom_to_keep':test_chroms,
    'chrom_threads':1,
    'labeling_approach':'peak_summit_in_bin_classification',
    'store_positives_only':False,
    'allow_ambiguous':True,
    }

genomewide_labels(train_params)
genomewide_labels(test_params)
