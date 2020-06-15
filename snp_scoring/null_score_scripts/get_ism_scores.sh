#!/bin/bash

for clust in {1..24}
    do
    echo Cluster $clust
    for fold in {0..9}
        do
        echo Fold $fold
        for shuf in {0..9}
            do
            echo Shuffle $shuf
            paste /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/shuffled_ism_scores/Cluster$clust/fold$fold.shuf$shuf.effect.scores /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/shuffled_ism_scores/Cluster$clust/fold$fold.shuf$shuf.noneffect.scores | awk 'BEGIN {OFS="\t"}{print $1, $2-$4}' > /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/shuffled_ism_scores/Cluster$clust/fold$fold.shuf$shuf.ism.scores
            done
        done
    done
