#!/bin/bash
#plink2 --pca 5 --allow-extra-chr --maf 0.05 --bfile /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/individual_bams/merged/merged --out /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/individual_bams/pca/adpd.merged.pca
plink2 --pca 5 --allow-extra-chr --maf 0.05 --bfile /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/individual_bams/merged/common.filtered --out /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/individual_bams/pca/adpd.1kg.merged.common.filtered.pca
