#!/bin/bash

# run asereadcounter to get counts at each SNP

# INPUT:
# BAMDIR = directory containning the bam files that we want to count SNPs on
# SAMPLE = name of sample for BAM file
# OUTDIR = output directory for current file
# MPILEUPDIR = VCF for variant calls on BAM file, output from 06_variant_calling.sh
# REF = path to reference fasta file to use

BAMDIR=$1
SAMPLE=$2
OUTDIR=$3
MPILEUPDIR=$4
REF=$5

INPUTBAM="${BAMDIR}/${SAMPLE}_adjustedheader.bam"
OUTFILE="${OUTDIR}/${SAMPLE}_asereadcounter.txt"

# Check if output file exists, if so, then don't run the script
if test -f ${OUTFILE};then
    exit 0
fi

# make sure input BAM exists and run asereadcounter
if test -f ${INPUTBAM}; then
    echo "processing ${INPUTBAM}"
    gatk ASEReadCounter \
        -R ${REF} \
        -I ${INPUTBAM} \
        -variant ${MPILEUPDIR}/chr1_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr2_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr3_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr4_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr5_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr6_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr7_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr8_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr9_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr10_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr11_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr12_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr13_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr14_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr15_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr16_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr17_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr18_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr19_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr20_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr21_mpileup_nodups.vcf \
        -variant ${MPILEUPDIR}/chr22_mpileup_nodups.vcf \
        -DF NotDuplicateReadFilter \
        --verbosity ERROR \
        -O ${OUTFILE}
fi
