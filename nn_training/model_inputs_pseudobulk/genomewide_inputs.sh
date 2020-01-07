##genomewide_labels --task_list sc.tasks.tsv \
#		  --outf classificationlabels.SummitWithin200bpCenter.hdf5 \
#		  --output_type hdf5 \
#		  --chrom_sizes /mnt/data/annotations/by_release/hg38/hg38.chrom.sizes \
#		  --bin_stride 50 \
#		  --left_flank 400 \
#		  --right_flank 400 \
#		  --bin_size 200 \
#		  --task_threads 1 \
#		  --chrom_threads 25 \
#		  --allow_ambiguous \
#		  --labeling_approach peak_summit_in_bin_classification \
#		  --split_output_by_task


genomewide_labels --task_list sc.tasks.tsv \
		  --outf Cluster24.regressionlabels.allbins.hg38.hdf5 \
		  --output_type hdf5 \
		  --chrom_sizes /mnt/data/annotations/by_release/hg38/hg38.chrom.sizes \
		  --bin_stride 50 \
		  --left_flank 400 \
		  --right_flank 400 \
		  --chrom_threads 25 \
		  --task_threads 2 \
		  --label_transformer asinh \
		  --labeling_approach all_genome_bins_regression \
		  --split_output_by_task

