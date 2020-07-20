#!/bin/bash

task=$1

obs_outdir=/mnt/lab_data3/soumyak/adpd/explain_scores
split_dir=split_scores
prefix=Cluster

for fold in {0..9}
do
    for allele in effect noneffect
    do
        ls $obs_outdir/$prefix$task/$split_dir/fold$fold.$allele.scores.split* | sort | xargs cat > $obs_outdir/$prefix$task/fold$fold.$allele.scores
    done
done

