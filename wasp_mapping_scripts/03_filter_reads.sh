#!/bin/bash
# this step filters out the reads where one or more of the allelic versions of the reads fail to map back to the same location as the original read

# INPUT:
# WASPDIR = path to WASP git director
# SAMPLE_NAME = name of read sample
# OUTDIR = output directory
# INTERSECTDIR = directory containing output from 01_intersect_snps.sh
# REMAPDIR = directory containing output from 02_remap_bowtie.sh

# ** NOTE: replace ".pe.q10.sort.rmdup.nodup.to.remap.bam" below with the filename ending

WASPDIR=$1
SAMPLE_NAME=$2
OUTDIR=$3
INTERSECTDIR=$4
REMAPDIR=$5

python ${WASPDIR}/mapping/filter_remapped_reads.py \
	${INTERSECTDIR}/${SAMPLE_NAME}.pe.q10.sort.rmdup.nodup.to.remap.bam \
	${REMAPDIR}/${SAMPLE_NAME}.sort.bam \
	${OUTDIR}/${SAMPLE_NAME}.keep.bam
