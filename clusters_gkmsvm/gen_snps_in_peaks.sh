#!/bin/bash

awk '{ if ($21 != "LD") { print } }' /mnt/lab_data2/annashch/alzheimers_parkinsons/ld_expand_snps_final/snps.hg19.bed.expanded > /mnt/lab_data3/soumyak/adpd/snp_lists/adpd/adpd.snps.hg19.bed.expanded

tail -n +2 /mnt/lab_data3/soumyak/adpd/snp_lists/adpd/adpd.snps.hg19.bed.expanded > /mnt/lab_data3/soumyak/adpd/snp_lists/adpd/for_bedtools.adpd.snps.hg19.bed.expanded

for peakfile in /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/idr_peaks/*.gz
do
    cluster=$(echo $peakfile | cut -d '/' -f 12 | cut -d '.' -f 1)
    echo $cluster

    head -n 1 /mnt/lab_data3/soumyak/adpd/snp_lists/adpd/adpd.snps.hg19.bed.expanded | cut -f 1,2,3,4,16,25 > /mnt/lab_data3/soumyak/adpd/snp_lists/adpd/idr_intersect/${cluster}.idr.adpd.snps.hg19.bed.expanded

    head -n 1 /mnt/lab_data3/soumyak/adpd/snp_lists/adpd/adpd.snps.hg19.bed.expanded | cut -f 1,2,3,4,16,25 > /mnt/lab_data3/soumyak/adpd/snp_lists/adpd/overlap_intersect/${cluster}.overlap.adpd.snps.hg19.bed.expanded

    bedtools intersect -u -wa -a /mnt/lab_data3/soumyak/adpd/snp_lists/adpd/for_bedtools.adpd.snps.hg19.bed.expanded -b /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/hg19_idr_peaks_bedtools_merged/${cluster}.idr.optimal.narrowPeak | sort -k1,1 -k 2,2 -k3,3 -k4,4 -k16,16 -k25,25 | bedtools groupby -g 1,2,3,4,16,25 -c 29 -o mean | cut -f 1,2,3,4,5,6 >> /mnt/lab_data3/soumyak/adpd/snp_lists/adpd/idr_intersect/${cluster}.idr.adpd.snps.hg19.bed.expanded

    bedtools intersect -u -wa -a /mnt/lab_data3/soumyak/adpd/snp_lists/adpd/for_bedtools.adpd.snps.hg19.bed.expanded -b /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/hg19_overlap_peaks_bedtools_merged/${cluster}.overlap.optimal.narrowPeak | sort -k1,1 -k 2,2 -k3,3 -k4,4 -k16,16 -k25,25 | bedtools groupby -g 1,2,3,4,16,25 -c 29 -o mean | cut -f 1,2,3,4,5,6 >> /mnt/lab_data3/soumyak/adpd/snp_lists/adpd/overlap_intersect/${cluster}.overlap.adpd.snps.hg19.bed.expanded

done
