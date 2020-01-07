#!/bin/bash
CLUSTER=$1
shift
GPU=$1
shift
[ -d /data/outputs/classification/Cluster$CLUSTER ] || mkdir -p /data/outputs/classification/Cluster$CLUSTER
CUDA_VISIBLE_DEVICES=$GPU kerasAC_cross_validate --index_data_path /data/inputs/Cluster$CLUSTER.classificationlabels.SummitWithin200bpCenter.hdf5 \
		    --input_data_path seq /data/inputs/gc_hg38_nosmooth.hdf5 \
		    --output_data_path /data/inputs/Cluster$CLUSTER.classificationlabels.SummitWithin200bpCenter.hdf5 \
		    --upsample_thresh_list_train 0 0.1 \
		    --upsample_ratio_list_train 0.7 \
		    --upsample_thresh_list_eval 0 0.1 \
		    --upsample_ratio_list_eval 0.98 \
		    --num_inputs 2 \
		    --num_outputs 1 \
		    --model_hdf5 /data/outputs/classification/Cluster$CLUSTER/DNASE.$CLUSTER.classificationlabels.withgc \
		    --ref_fasta /data/inputs/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta \
		    --batch_size 200 \
		    --architecture_spec functional_basset_classification_gc_corrected \
		    --num_train 1000000 \
		    --num_valid 1000000 \
		    --num_tasks 1 \
		    --threads 10 \
		    --max_queue_size 100 \
		    --init_weights /data/inputs/encode-roadmap.dnase_tf-chip.batch_256.params.npz \
		    --patience 1 \
		    --patience_lr 2 \
		    --expand_dims \
		    --predictions_and_labels_hdf5 /data/outputs/classification/Cluster$CLUSTER/predictions.DNASE.$CLUSTER.classificationlabels.withgc \
		    --performance_metrics_classification_file /data/outputs/classification/Cluster$CLUSTER/performance.DNASE.$CLUSTER.classificationlabels.withgc \
		    --tasks Cluster$CLUSTER gc_fract \
		    --index_tasks Cluster$CLUSTER \
		    --splits "$@"

