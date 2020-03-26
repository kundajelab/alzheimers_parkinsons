#!/bin/bash

samtools mpileup -f /mnt/lab_data3/soumyak/refs/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta -l /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allele_bias/snps/hg38_snps_1KG_ADPD.bed $1 | gzip > /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allele_bias/quasar/pileup/${2}.pileup.gz


