#!/bin/bash
for cluster in 1 2 3 4 13 14 15 16
do
    python summarize.py --input_pickle buddies.Cluster$cluster.fold0.classification \
       --cluster $cluster \
       --fold 0 \
       --regression_classification classification \
       --snp_flank 10 \
       --sig_snps SigSNPs_AllClusters_MergedUnique.csv
    python summarize.py --input_pickle buddies.Cluster$cluster.fold0.regression \
       --cluster $cluster \
       --fold 0 \
       --regression_classification regression \
       --snp_flank 10 \
       --sig_snps SigSNPs_AllClusters_MergedUnique.csv
done
