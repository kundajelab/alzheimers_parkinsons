#!/bin/bash
for cluster in 24 #`seq 2 24`
do
    for fold in `seq 0 9`
    do
	python make_plots.py --input_pickle_classification sig.snps.Cluster$cluster.fold$fold.classification \
	       --input_pickle_regression sig.snps.Cluster$cluster.fold$fold.regression \
	       --cluster $cluster \
	       --fold $fold &
    done
done
