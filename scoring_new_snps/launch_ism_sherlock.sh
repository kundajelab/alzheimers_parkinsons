#!/bin/bash

for i in {1..24}
    do
    for j in {0..9}
        do
        sbatch --export=ALL -c 16 -t 2:00:00 -p akundaje -J C${i}_F${j} -o /home/groups/akundaje/soumyak/alzheimers_parkinsons/scoring_new_snps/logs/ism/cluster${i}_fold${j}.o -e /home/groups/akundaje/soumyak/alzheimers_parkinsons/scoring_new_snps/logs/ism/cluster${i}_fold${j}.e run_ism.sh $i $j
        done
    done
