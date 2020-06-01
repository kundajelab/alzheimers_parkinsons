#!/bin/bash


# this script remaps the reads that WASP identifies
# we need to use the same aligner and arguments that were used for the original mapping to create the input BAM files

# From WASP:
# Map the PREFIX.remap.fq.gz using the same mapping arguments used in Step 1. Note that the arguments should be exactly the same as those in Step 1 EXCEPT for arguments that directly modify the reads that are used by the aligner. For example the read trimming arguments to bowtie (-3 and -5 arguments) should be used in Step 1 ONLY, because they modify the reads that are output by bowtie.


# SAMPLE_NAME = name for sample for reads
# INTERSECTDIR = directory containing output from 01_intersect_snps.sh
# OUTDIR = output directory
# GENOMEFILE = Bowtie2 indexed reference genome file to map reads to

# ** NOTE: replace ".pe.q10.sort.rmdup.nodup.to.remap.bam" below with file ending 

SAMPLE_NAME=$1
INTERSECTDIR=$2
OUTDIR=$3

GENOMEFILE=$4

bowtie2-align-s --wrapper basic-0 \
	-p 16 \
	--very-sensitive \
	-X 2000 \
	--rg-id ${SAMPLE_NAME} \
	-x ${GENOMEFILE} \
	-1 ${INTERSECTDIR}/${SAMPLE_NAME}.pe.q10.sort.rmdup.nodup.remap.fq1.gz \
	-2 ${INTERSECTDIR}/${SAMPLE_NAME}.pe.q10.sort.rmdup.nodup.remap.fq2.gz \
	| samtools view -b > ${OUTDIR}/${SAMPLE_NAME}.bam


samtools sort -o ${OUTDIR}/${SAMPLE_NAME}.sort.bam ${OUTDIR}/${SAMPLE_NAME}.bam
samtools index ${OUTDIR}/${SAMPLE_NAME}.sort.bam
