#!/bin/bash

for clust in {1..24}
    do
    echo Cluster $clust
    for fold in {0..9}
        do
        echo Fold $fold
        paste /home/groups/akundaje/soumyak/alzheimers_parkinsons/scoring_new_snps/ism_scores/Cluster$clust/fold$fold.effect.scores /home/groups/akundaje/soumyak/alzheimers_parkinsons/scoring_new_snps/ism_scores/Cluster$clust/fold$fold.noneffect.scores | awk 'BEGIN {OFS="\t"}{print $1, $2-$4}' > /home/groups/akundaje/soumyak/alzheimers_parkinsons/scoring_new_snps/ism_scores/Cluster$clust/fold$fold.ism.scores
        done
    done
