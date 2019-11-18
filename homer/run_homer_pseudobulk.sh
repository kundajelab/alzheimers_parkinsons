#!/bin/bash
module load homer 
#findMotifsGenome.pl diff_pd_caud_adpd_vs_ctrl_up.bed hg38 diff_pd_caud_adpd_vs_ctrl_up -bg background.idr.bed &
#findMotifsGenome.pl diff_pd_caud_adpd_vs_ctrl_down.bed hg38 diff_pd_caud_adpd_vs_ctrl_down -bg background.idr.bed & 

#findMotifsGenome.pl expanded_diff_pd_caud_gba1_vs_ctrl_up.bed hg38 expanded_diff_pd_caud_gba1_vs_ctrl_up -bg background.idr.bed &
#findMotifsGenome.pl expanded_diff_pd_caud_gba1_vs_ctrl_down.bed hg38 expanded_diff_pd_caud_gba1_vs_ctrl_down -bg background.idr.bed &
prefix=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk

#genome background idr 
#for cluster in `seq 1 24`
#do
#    findMotifsGenome.pl  $prefix/pseudobulk_outputs/peaks/idr_peaks_bedtools_merged/Cluster$cluster.idr.optimal.narrowPeak hg38 $prefix/homer/background_genome_idr/Cluster$cluster &
#done

#cluster background idr 
#for cluster in `seq 1 24`
#do
#    findMotifsGenome.pl  $prefix/pseudobulk_outputs/peaks/idr_peaks_bedtools_merged/Cluster$cluster.idr.optimal.narrowPeak hg38 $prefix/homer/background_clusters_idr/Cluster$cluster -bg pseudobulk.idr.bedtools.merged.background.bed &
#done

#genome background overlap
#for cluster in `seq 1 24`
#do
#    findMotifsGenome.pl  $prefix/pseudobulk_outputs/peaks/overlap_peaks_bedtools_merged/Cluster$cluster.overlap.optimal.narrowPeak hg38 $prefix/homer/background_genome_overlap/Cluster$cluster 
#done

#cluster background overlap 
for cluster in `seq 1 24`
do
    findMotifsGenome.pl  $prefix/pseudobulk_outputs/peaks/overlap_peaks_bedtools_merged/Cluster$cluster.overlap.optimal.narrowPeak hg38 $prefix/homer/background_clusters_overlap/Cluster$cluster -bg pseudobulk.overlap.bedtools.merged.background.bed &
done




