#!/bin/bash

for file in /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/output/*; do
    sbatch --partition akundaje --mem=30G -o /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/snps/${file:76:12}.snps.vcf.gz \
    -e /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/log/${file:76:12}.snps.e \
    -n 1 --ntasks-per-node=1 --job-name=${file:76:12} --time=48:00:00 --cpus-per-task=2 \
    run_snps.sh $file
done
