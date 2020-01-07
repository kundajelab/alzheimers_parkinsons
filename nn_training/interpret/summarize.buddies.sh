#!/bin/bash
#for cluster in 1 2 3 4 13 14 15 16
for cluster in 5 6 7 8 9 10 11 12 17 18 19 20 21 22 23 24
do
    python summarize.py --input_pickle pickles_buddies/buddies.Cluster$cluster.fold0.classification \
       --cluster $cluster \
       --fold 0 \
       --regression_classification classification \
       --snp_flank 10 \
       --sig_snps SigSNPs_AllClusters_MergedUnique.csv \
       --out_prefix summaries_buddies/
    python summarize.py --input_pickle pickles_buddies/buddies.Cluster$cluster.fold0.regression \
       --cluster $cluster \
       --fold 0 \
       --regression_classification regression \
       --snp_flank 10 \
       --sig_snps SigSNPs_AllClusters_MergedUnique.csv \
       --out_prefix summaries_buddies/
done
