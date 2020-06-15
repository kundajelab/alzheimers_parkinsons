#!/bin/bash

for peakfile in /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/idr_peaks/*.gz
do
    cluster=$(echo $peakfile | cut -d '/' -f 12 | cut -d '.' -f 1)
    echo $cluster
    #mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}
    for f in 0 1 2 3 4 5 6 7 8 9
    do
        echo fold${f}

        #mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}
        #mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/train
        #mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/test
        #mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/explain
        #mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/explain/input/
        #mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/explain/output/
        #mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/explain/input/major
        #mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/explain/input/minor
        #mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/explain/input/dnshuff/
        #mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/explain/output/major
        #mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/explain/output/minor
        #mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/explain/output/dnshuff/
        #mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/gwas
        mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/gwas/idr
        mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/gwas/overlap


    done

    #mkdir /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/peaks
    #zcat $peakfile | bedtools groupby -g 1,2,3 -c 8,10 -o collapse,collapse > /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/peaks/all_idr_peaks.bed

done
