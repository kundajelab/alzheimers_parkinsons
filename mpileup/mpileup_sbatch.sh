#!/bin/bash

for file in /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/merged_bams/*; do
    sbatch --partition akundaje --mem=30G -o /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/output/${file:73:12}.vcf.gz \
    -e /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/log/${file:73:12}.e \
    -n 1 --ntasks-per-node=1 --job-name=${file:73:12} --time=48:00:00 --cpus-per-task=2 \
    run_mpileup.sh $file
done
