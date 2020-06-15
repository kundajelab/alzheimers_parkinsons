#!/bin/bash

for i in {1..24}
    do
        sbatch --export=ALL -c 10 -t 2:00:00 -p akundaje -J C${i} -o /home/groups/akundaje/soumyak/alzheimers_parkinsons/scoring_new_snps/logs/delta/cluster${i}.o -e /home/groups/akundaje/soumyak/alzheimers_parkinsons/scoring_new_snps/logs/delta/cluster${i}.e run_deltasvm.sh $i
    done
