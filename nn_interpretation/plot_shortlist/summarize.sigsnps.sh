#!/bin/bash
for cluster in `seq 1 24`
do
    python summarize.py --input_pickle sig.snps.Cluster$cluster.fold0.classification \
       --cluster $cluster \
       --fold 0 \
       --regression_classification classification \
       --snp_flank 10 \
       --sig_snps SigSNPs_AllClusters_MergedUnique.csv \
       --out_prefix sig.
    python summarize.py --input_pickle sig.snps.Cluster$cluster.fold0.regression \
       --cluster $cluster \
       --fold 0 \
       --regression_classification regression \
       --snp_flank 10 \
       --sig_snps SigSNPs_AllClusters_MergedUnique.csv \
       --out_prefix sig.
done

