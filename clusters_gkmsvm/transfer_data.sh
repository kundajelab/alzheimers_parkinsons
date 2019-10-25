#!/bin/bash

kinit soumyak
mkdir /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm

for peakfile in /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/idr_peaks/*.gz
do
    cluster=$(echo $peakfile | cut -d '/' -f 12 | cut -d '.' -f 1)
    echo $cluster
    mkdir /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}
    for f in 0 1 2 3 4 5 6 7 8 9
    do
        echo fold${f}

        mkdir /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}
        mkdir /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}/train
        mkdir /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}/test
        mkdir /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}/explain
        mkdir /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}/explain/input
        mkdir /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}/explain/output
        mkdir /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}/explain/input/ref
        mkdir /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}/explain/input/alt
        mkdir /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}/explain/input/dnshuff
        mkdir /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}/explain/output/ref
        mkdir /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}/explain/output/alt
        mkdir /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}/explain/output/dnshuff

        rsync -P /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/train/train.final.pos.fasta /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}/train/
        rsync -P /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/train/train.final.neg.fasta /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}/train/
        rsync -P /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/test/test.final.pos.fasta /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}/test/
        rsync -P /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/${cluster}/fold${f}/test/test.final.neg.fasta /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/${cluster}/fold${f}/test/

    done

done
