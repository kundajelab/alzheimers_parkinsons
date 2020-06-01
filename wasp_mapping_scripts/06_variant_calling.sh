#!/bin/bash
# call variants from wasp corrected bam files

# INPUT:
# OUTFILE = directory for current output
# BAMDIR = directory containing WASP output, from 05_filter_duplicate_reads.sh
# REGIONSFILE = regions to call SNPs 
# REFFILE = file containing reference genome

OUTFILE=$1
BAMDIR=$2
REGIONSFILE=$3
REFFILE=$4



# adjust this to allow more bam files to be read as input
dirlist=`ls ${BAMDIR}/*.bam`


# used for timing the entire process
SECONDS=0

bcftools mpileup -Ou -B \
	--max-depth 1000 \
    -R $REGIONSFILE \
    --skip-indels \
	-f $REFFILE \
	--threads 1 \
	${dirlist} \
	| bcftools call -mv -Ob --threads 1 \
    | bcftools sort \
	| bcftools view \
	> $OUTFILE

# gives time for process
duration=$SECONDS
echo "Total of $(($duration / 60)) and $(($duration % 60)) seconds elapsed for process"


# index the bam files
./index_vcfs.sh $OUTFILE
