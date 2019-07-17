#split 0
#CUDA_VISIBLE_DEVICES=3 kerasAC_train --nonzero_bin_path /mnt/lab_data2/annashch/alzheimers_parkinsons/model_inputs/input.hdf5 \
#		    --universal_negative_path /mnt/lab_data2/annashch/alzheimers_parkinsons/model_inputs/universal_negatives.input.hdf5 \
#		    --model_hdf5 adpd.regression.0 \
#		    --batch_size 1000 \
#		    --train_upsample 0.3 \
#		    --train_chroms chr2 chr3 chr4 chr5 chr6 chr7 chr9 chr11 chr12 chr13 chr14 chr15 chr16 chr17 chr18 chr19 chr20 chr21 chr22 chrX chrY \
#		    --validation_chroms chr8 chr10 \
#		    --architecture_spec regression \
#		    --tensorboard_logdir logs \
#		    --tensorboard \
#		    --num_train 50000 \
#		    --num_valid 50000 \
#		    --num_tasks 1 \
#		    --threads 40 \
#		    --max_queue_size 200 \
#		    --init_weights /srv/scratch/annashch/deeplearning/encode-roadmap.dnase_tf-chip.batch_256.params.npz \
#		    --patience 3 \
#		    --patience_lr 2 \
#		    --ref_fasta /mnt/data/annotations/by_release/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta \
#		    --tasks PD_CTRL_MDTG
#
CUDA_VISIBLE_DEVICES=0 kerasAC_predict  --nonzero_bin_path /mnt/lab_data2/annashch/alzheimers_parkinsons/model_inputs/input.hdf5 \
		    --universal_negative_path /mnt/lab_data2/annashch/alzheimers_parkinsons/model_inputs/universal_negatives.input.hdf5 \
		    --model_hdf5 adpd.regression.0 \
		    --batch_size 1000 \
		    --predict_chroms chr1 \
		    --threads 40 \
		    --max_queue_size 5000 \
		    --performance_metrics_regression_file metrics.0 \
		    --predictions_pickle predictions.0 \
		    --ref_fasta /mnt/data/annotations/by_release/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta \
		    --tasks PD_CTRL_MDTG


