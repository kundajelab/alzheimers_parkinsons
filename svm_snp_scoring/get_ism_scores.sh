#!/bin/bash

for i in {1..24}
    do
        echo Cluster $i
        for j in {0..9}
            do
                echo Fold $j
                paste /mnt/lab_data3/soumyak/adpd/ism_scores/Cluster$i/fold$j.effect.scores /mnt/lab_data3/soumyak/adpd/ism_scores/Cluster$i/fold$j.noneffect.scores | awk 'BEGIN {OFS="\t"}{print $1, $2-$4}' > /mnt/lab_data3/soumyak/adpd/ism_scores/Cluster$i/fold$j.ism.scores
            done
    done
