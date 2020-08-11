#!/bin/bash

task=$1

null_outdir=/mnt/lab_data3/soumyak/adpd/null_explain_scores
split_dir=split_scores
prefix=Cluster

for fold in {0..9}
do
    for allele in effect noneffect
    do
        for null in {0..9}
        do
            ls $null_outdir/$prefix$task/$split_dir/fold$fold.null$null.$allele.scores.split* | sort | xargs cat > $null_outdir/$prefix$task/fold$fold.null$null.$allele.scores
        done
    done
done

