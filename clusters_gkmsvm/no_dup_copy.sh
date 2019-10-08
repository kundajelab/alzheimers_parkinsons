#!/bin/bash

for peakfile in /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/idr_peaks/*.gz
do
    cluster=$(echo $peakfile | cut -d '/' -f 12 | cut -d '.' -f 1)
    echo $cluster
    for fold in {0..9}
    do
        echo fold$fold
        if test -f /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/$cluster/fold$fold/train/train.output.model.txt; then
            model=/oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/$cluster/fold$fold/train/train.output.model.txt
            if test -f /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/$cluster/fold$fold/train/train.output.model.txt; then
                echo "Model Exists"
            else
                #cp $model /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/$cluster/fold$fold/train/
                echo "Copying Model"
            fi
        fi
        if test -f /oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/$cluster/fold$fold/test/accuracy.txt; then
            acc=/oak/stanford/groups/akundaje/soumyak/clusters_gkmsvm/$cluster/fold$fold/test/accuracy.txt
            if test -f /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/$cluster/fold$fold/test/accuracy.txt; then
                echo "Results Exist"
            else
                #cp $acc /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/$cluster/fold$fold/test/
                echo "Copying Results"
            fi
        fi
    done
done
