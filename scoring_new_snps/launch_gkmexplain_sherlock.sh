#!/bin/bash

for i in 16 24 #{1..24}
    do
    for j in 0 9 #{0..9}
        do
        sbatch --export=ALL -t 2:00:00 -p akundaje -J C${i}_F${j} -o /home/groups/akundaje/soumyak/alzheimers_parkinsons/scoring_new_snps/logs/explain/cluster${i}_fold${j}.o -e /home/groups/akundaje/soumyak/alzheimers_parkinsons/scoring_new_snps/logs/explain/cluster${i}_fold${j}.e run_gkmexplain.sh $i $j
        done
    done
