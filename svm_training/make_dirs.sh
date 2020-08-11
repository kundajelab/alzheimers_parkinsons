#!/bin/bash

mkdir /mnt/lab_data3/soumyak/adpd/gkmsvm

cp -r /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/idr_peaks /mnt/lab_data3/soumyak/adpd/
cp -r /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/ambiguous /mnt/lab_data3/soumyak/adpd/

gunzip /mnt/lab_data3/soumyak/adpd/idr_peaks/Cluster*.gz
gunzip /mnt/lab_data3/soumyak/adpd/ambiguous/Cluster*.gz

for peakfile in /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/idr_peaks/*.gz
do
    cluster=$(echo $peakfile | cut -d '/' -f 12 | cut -d '.' -f 1)
    echo $cluster
    mkdir /mnt/lab_data3/soumyak/adpd/gkmsvm/${cluster}
    for f in 0 1 2 3 4 5 6 7 8 9
    do
        echo fold${f}

        mkdir /mnt/lab_data3/soumyak/adpd/gkmsvm/${cluster}/fold${f}
        mkdir /mnt/lab_data3/soumyak/adpd/gkmsvm/${cluster}/fold${f}/train
        mkdir /mnt/lab_data3/soumyak/adpd/gkmsvm/${cluster}/fold${f}/test

    done

    mkdir /mnt/lab_data3/soumyak/adpd/gkmsvm/${cluster}/peaks
    zcat $peakfile | bedtools groupby -g 1,2,3 -c 8,10 -o collapse,collapse > /mnt/lab_data3/soumyak/adpd/gkmsvm/${cluster}/peaks/all_idr_peaks.bed

done
