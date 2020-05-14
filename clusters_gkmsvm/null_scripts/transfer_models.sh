#!/bin/bash

for i in {1..24}
    do
    echo Cluster $i
    mkdir /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/svm_models/Cluster${i}
    for j in {0..9}
        do
        echo Fold $j
        cp /mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster${i}/fold${j}/train/train.output.model.txt /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/svm_models/Cluster${i}/fold${j}.model.txt
        done
    done
