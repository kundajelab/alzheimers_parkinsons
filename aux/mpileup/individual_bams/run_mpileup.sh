#!/bin/bash
input_bam=$1
output=$2
ref=$3
#bcftools mpileup -f $ref -O b -o $output $input_bam 
bcftools index $output
 
