#!/bin/bash

# this file calls the find_intersecting_snps.py file from WASP
# 
# We assume that we already have the mapped bam file and will look for 
# intersection with the SNP files that we generated

# INPUT:
# SNPDIR = directory containg SNPs of interest
# OUTDIR = output directory
# BAMDIR = directory containing input BAM files
# WASPPATH = path to WASP git folder


SNPDIR=$1
OUTDIR=$2
BAMPATH=$3
WASPPATH=$4

python ${WASPPATH}/mapping/find_intersecting_snps.py \
	--is_sorted \
	--is_paired \
	--snp_dir $SNPDIR \
	--output_dir $OUTDIR \
    $BAMPATH
