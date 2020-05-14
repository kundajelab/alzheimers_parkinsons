#!/bin/bash

zcat /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allelic_imbalance/quasar/pileup/${1}.pileup.gz | awk -v OFS='\t' '{ if ($4>0 && $5 !~ /[^\^][<>]/ && $5 !~ /\+[0-9]+[ACGTNacgtn]+/ && $5 !~ /-[0-9]+[ACGTNacgtn]+/ && $5 !~ /[^\^]\*/) print $1,$2-1,$2,$3,$4,$5,$6}' | sortBed -i stdin | intersectBed -a stdin -b /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allelic_imbalance/snps/hg38_snps_1KG_ADPD.bed -wo | cut -f 1-7,11-14 | gzip > /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allelic_imbalance/quasar/pileup_bed/${1}.pileup.bed.gz

