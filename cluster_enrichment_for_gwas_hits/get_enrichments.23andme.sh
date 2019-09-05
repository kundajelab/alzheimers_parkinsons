#!/bin/bash
python get_enrichments.py --peak_bed idr_peaks_bedtools_merged/*narrowPeak \
       --gwas_thresh_bed 23andme.-*bed \
       --gwas_all_bed 23andme.bed \
       --outf cluster.enrichments.23andme.idr.txt &
python get_enrichments.py --peak_bed overlap_peaks_bedtools_merged/*narrowPeak \
       --gwas_thresh_bed 23andme.-*bed \
       --gwas_all_bed 23andme.bed \
       --outf cluster.enrichments.23andme.overlap.txt &
python get_enrichments.py --peak_bed celltype_idr_peaks_bedtools_merged/*narrowPeak \
       --gwas_thresh_bed 23andme.-*bed \
       --gwas_all_bed 23andme.bed \
       --outf celltype.enrichments.23andme.idr.txt &
python get_enrichments.py --peak_bed celltype_overlap_peaks_bedtools_merged/*narrowPeak \
       --gwas_thresh_bed 23andme.-*bed \
       --gwas_all_bed 23andme.bed \
       --outf celltype.enrichments.23andme.overlap.txt &
