task=$1
for split in `seq 0 9`
do
    for dataset in train test
    do
	python /srv/scratch/annashch/5_cell_lines_bias_correction/genomewide_gc/get_gc_content.py \
	       --input_bed $task.svm.peaks.$dataset.$split \
	       --ref_fasta /mnt/data/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta \
	       --out_prefix $task.svm.peaks.$dataset.$split.gc.seq \
	       --center_summit \
	       --flank_size 500 \
	       --store_seq &
    done
done
