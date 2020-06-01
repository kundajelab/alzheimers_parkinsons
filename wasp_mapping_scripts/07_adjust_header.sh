#!/bin/bash

# adjust the header for the output bams from WASP

# this file creates two temp files in the current directory 
# these are deleted at the end
# temp files are temp.txt and header.txt - if these already exist, it will write over them and delete them!


# INPUT:
# BAMDIR = directory containing BAM files which were outpu by WASP
# SAMPLE = name of sample
# OUTPUT = output directory of current file

# ** NOTE: adjust BAMEFILE name ending if needed


BAMDIR=$1
SAMPLE=$2
OUTDIR=$3

BAMFILE="${BAMDIR}/${SAMPLE}.keep.merge.rmdup.sort.bam"
OUTBAM="${OUTDIR}/${SAMPLE}_adjustedheader.bam"

TEMP1="temp1_${SAMPLE}.txt"
TEMP2="temp2_${SAMPLE}.txt"

# get the RG lines from header and attach other fields, save in temp file
samtools view -H $BAMFILE | grep '@RG' > $TEMP1
sed -e 's/$/\tPL:foo\tLB:foo\tSM:sample/' -i $TEMP1

# get header without RG lines
samtools view -H $BAMFILE | grep -v '@RG' > $TEMP2
cat $TEMP1 >> $TEMP2
samtools reheader -P $TEMP2 $BAMFILE > $OUTBAM 

# index the bam file
samtools index $OUTBAM

# remove the temp files
rm $TEMP1
rm $TEMP2
