#!/bin/bash

for i in {1..24}
    do
    for j in {0..9}
        do
        sbatch --export=ALL -c 10 -t 5-0 -p akundaje -J Cluster${i}_Fold${j} -o /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/shuffled_logs/explain/cluster${i}_fold${j}.o -e /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/shuffled_logs/explain/cluster${i}_fold${j}.e run_gkmexplain.sh $i $j
        done
    done
