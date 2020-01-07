#!/bin/bash
for cluster in 24 
do
    for fold in 3 4
    do
	CUDA_VISIBLE_DEVICES=1 python interpret_gradxinput_and_ism.py \
		    	--bed_path=/srv/scratch/annashch/deeplearning/adpd/interpret/nn_unique.buddies.tsv \
			--ref_allele_col noneffect_allele \
			--alt_allele_col effect_allele \
			--compute_gc \
			--flank_size 500 \
			--chrom_col chr \
			--pos_col pos \
			--rsid_col rsid \
			--ref_fasta /mnt/data/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta \
			--batch_size 1000 \
			--model_string /srv/scratch/annashch/deeplearning/adpd/microglia_gc/regression/ADPD.Cluster24.pseudobulk.regressionlabels.withgc.$fold \
			--target_layer_idx -1 \
			--outf nn_unique.Cluster$cluster.fold$fold.regression

    done
done
