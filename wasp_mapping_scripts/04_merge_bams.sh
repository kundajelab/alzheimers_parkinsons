#!/bin/bash

# this step merges the keep bam and the remapped bam files for a complete set of mappability-filtered aligned reads
# we then sort and index the merged file

# INPUT:
# FILTERDIR: directory containing output from 03_filter_reads.sh
# INTERSECTDIR: directory containing output from 01_intersect_snps.sh
# MERGEDIR: output directory
# SAMPLE_NAME: name of sample for reads

FILTERDIR=$1
INTERSECTDIR=$2
MERGEDIR=$3
SAMPLE_NAME=$4

samtools merge ${MERGEDIR}/${SAMPLE_NAME}.keep.merge.bam \
              ${FILTERDIR}/${SAMPLE_NAME}.keep.bam  \
              ${INTERSECTDIR}/${SAMPLE_NAME}.pe.q10.sort.rmdup.nodup.keep.bam

samtools sort -o  ${MERGEDIR}/${SAMPLE_NAME}.keep.merge.sort.bam \
              ${MERGEDIR}/${SAMPLE_NAME}.keep.merge.bam 

samtools index ${MERGEDIR}/${SAMPLE_NAME}.keep.merge.sort.bam
