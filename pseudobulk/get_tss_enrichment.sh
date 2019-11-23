#!/bin/bash
python /users/annashch/anna_utils/atac_and_rna_analysis/encode_task_tss_enrich.py --read-len 99 \
       --nodup-bam /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_bam/Cluster$1.bam \
       --chrsz /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/hg38.chrom.sizes \
       --tss /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/tss.pc.gencode.v29.bed.gz \
       --out-dir /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_tss/Cluster$1
