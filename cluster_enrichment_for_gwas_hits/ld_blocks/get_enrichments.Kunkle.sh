#!/bin/bash

python get_enrichments.py --peak_bed ../idr_peaks_bedtools_merged/*narrowPeak \
       --gwas_thresh_bed Kunkle.blocks.-*bed \
       --gwas_all_bed fourier_ls-all.bed \
       --outf cluster.enrichments.Kunkle.idr.txt 
python get_enrichments.py --peak_bed ../overlap_peaks_bedtools_merged/*narrowPeak \
       --gwas_thresh_bed Kunkle.blocks.-*bed \
       --gwas_all_bed fourier_ls-all.bed \
       --outf cluster.enrichments.Kunkle.overlap.txt 
python get_enrichments.py --peak_bed ../celltype_idr_peaks_bedtools_merged/*narrowPeak \
       --gwas_thresh_bed Kunkle.blocks.-*bed \
       --gwas_all_bed fourier_ls-all.bed \
       --outf celltype.enrichments.Kunkle.idr.txt 
python get_enrichments.py --peak_bed ../celltype_overlap_peaks_bedtools_merged/*narrowPeak \
       --gwas_thresh_bed Kunkle.blocks.-*bed \
       --gwas_all_bed fourier_ls-all.bed \
       --outf celltype.enrichments.Kunkle.overlap.txt 
