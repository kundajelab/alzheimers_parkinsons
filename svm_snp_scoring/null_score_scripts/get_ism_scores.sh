#!/bin/bash

for clust in 1 24
    do
    echo Cluster $clust
    for fold in {0..9}
        do
        echo Fold $fold
        for shuf in {0..9}
            do
            echo Shuffle $shuf
            paste /mnt/lab_data3/soumyak/adpd/null_ism_scores/Cluster$clust/fold$fold.null$shuf.effect.scores /mnt/lab_data3/soumyak/adpd/null_ism_scores/Cluster$clust/fold$fold.null$shuf.noneffect.scores | awk 'BEGIN {OFS="\t"}{print $1, $2-$4}' > /mnt/lab_data3/soumyak/adpd/null_ism_scores/Cluster$clust/fold$fold.null$shuf.ism.scores
            done
        done
    done
