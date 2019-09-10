#!/bin/bash

for peakfile in /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/idr_peaks/*.gz
do
    cluster=$(echo $peakfile | cut -d '/' -f 12 | cut -d '.' -f 1)
    echo $cluster
    #mkdir /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}
    for f in 0 1 2 3 4 5 6 7 8 9
    do
        echo fold${f}

        rm -r /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}/explain/output/ref/importance
        rm -r /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}/explain/output/alt/importance
        rm -r /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}/explain/output/ref/hypothetical
        rm -r /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}/explain/output/alt/hypothetical

        #mkdir /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}
        #mkdir /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}/train
        #mkdir /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}/test
        #mkdir /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}/explain
        #mkdir /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}/explain/input/
        #mkdir /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}/explain/output/
        #mkdir /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}/explain/input/ref
        #mkdir /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}/explain/input/alt
        #mkdir /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}/explain/input/dnshuff/
        #mkdir /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}/explain/output/ref
        #mkdir /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}/explain/output/alt
        #mkdir /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/fold${f}/explain/output/dnshuff/

    done

    #mkdir /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/peaks
    #zcat $peakfile | bedtools groupby -g 1,2,3 -c 8,10 -o collapse,collapse > /mnt/lab_data3/soumyak/adpd/gkmSVM/${cluster}/peaks/all_idr_peaks.bed

done
