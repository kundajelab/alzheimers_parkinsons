#!/bin/bash

for i in {1..24}
    do
    for j in {0..9}
        do
        sbatch --export=AL -c 10 -t 5-0 -p akundaje -J Cluster${i}_Fold${j} run_explain.sh $i $j
        done
    done
