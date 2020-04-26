#!/bin/bash

for i in {1..24}
    do
    for j in {0..9}
        do
        sbatch --export=ALL -c 16 -t 1-0 -p akundaje -J C${i}_F${j} -o /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/shuffled_logs/ism/cluster${i}_fold${j}.o -e /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/shuffled_logs/ism/cluster${i}_fold${j}.e run_ism.sh $i $j
        done
    done
