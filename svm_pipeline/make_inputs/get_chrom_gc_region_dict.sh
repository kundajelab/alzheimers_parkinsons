task=$1
python get_chrom_gc_region_dict.py --input_bed $task.candidate.negatives.tsv --outf $task.candidate.negatives.gc.p
