#!/bin/bash

# this file filters duplicate reads in an unbiased way

# Filter duplicate reads. Programs such as samtools rmdup introduce bias when they filter duplicate reads because they retain the read with the highest score (which usually matches the reference). We provide a script rmdup.py which performs unbiased removal of duplicate reads. The script discards duplicate reads at random (independent of their score). The input BAM or SAM file must be sorted.

# INPUT:
# WASPDIR = directory for WASP git 
# MERGEDIR = directory containing output from 04_merge_bams.sh
# SAMPLE_NAME = name of sample for reads
# RMDUPDIR = output for current file


WASPDIR=$1
MERGEDIR=$2
SAMPLE_NAME=$3
RMDUPDIR=$4


python ${WASPDIR}/mapping/rmdup_pe.py \
	${MERGEDIR}/${SAMPLE_NAME}.keep.merge.sort.bam \
	${MERGEDIR}/${SAMPLE_NAME}.keep.merge.rmdup.bam

samtools sort -o ${RMDUPDIR}/${SAMPLE_NAME}.keep.merge.rmdup.sort.bam \
	${MERGEDIR}/${SAMPLE_NAME}.keep.merge.rmdup.bam

samtools index ${RMDUPDIR}/${SAMPLE_NAME}.keep.merge.rmdup.sort.bam
