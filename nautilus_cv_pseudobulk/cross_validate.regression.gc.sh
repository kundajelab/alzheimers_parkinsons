#!/bin/bash
CLUSTER=$1
GPU=$2
[ -d /data/outputs/Cluster$CLUSTER ] || mkdir -p /data/outputs/Cluster$CLUSTER
CUDA_VISIBLE_DEVICES=$GPU kerasAC_cross_validate --index_data_path /data/inputs/Cluster$CLUSTER.regressionlabels.allbins.hg38.hdf5 \
		    --input_data_path seq /data/inputs/gc_hg38_nosmooth.hdf5 \
		    --output_data_path /data/inputs/Cluster$CLUSTER.regressionlabels.allbins.hg38.hdf5 \
		    --upsample_thresh_list_train 0 0.1 \
		    --upsample_ratio_list_train 0.7 \
		    --upsample_thresh_list_eval 0 0.1 \
		    --upsample_ratio_list_eval 0.98 \
		    --num_inputs 2 \
		    --num_outputs 1 \
		    --model_hdf5 /data/outputs/regression/Cluster$CLUSTER/DNASE.$CLUSTER.regressionlabels.withgc \
		    --ref_fasta /data/inputs/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta \
		    --batch_size 200 \
		    --architecture_spec functional_basset_regression_gc_corrected \
		    --num_train 1000000 \
		    --num_valid 1000000 \
		    --num_tasks 1 \
		    --threads 10 \
		    --max_queue_size 100 \
		    --init_weights /data/inputs/encode-roadmap.dnase_tf-chip.batch_256.params.npz \
		    --patience 1 \
		    --patience_lr 2 \
		    --expand_dims \
		    --predictions_and_labels_hdf5 /data/ouptputs/regression/Cluster$CLUSTER/predictions.DNASE.$CLUSTER.regressionlabels.withgc \
		    --performance_metrics_regression_file /data/outputs/regression/Cluster$CLUSTER/performance.DNASE.$CLUSTER.regressionlabels.withgc \
		    --tasks Cluster$CLUSTER gc_fract \
		    --index_tasks Cluster$CLUSTER





