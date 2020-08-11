#!/bin/bash

bash make_dirs.sh   # Make all directories for SVM SNP scoring

python get_snps_in_peaks.py     # Get SNPs in overlap peaks for each cluster

python get_ism_inputs.py        # Get input sequences for ISM and deltaSVM

python get_gkmexplain_inputs.py # Get input sequences for GkmExplain

python schedule_ism.py 1 24 40  # Run gkmpredict for ISM scores

bash get_ism_scores.sh          # Get ISM scores

for i in {1..24}
do
    python schedule_gkmexplain.sh $i   # Run GkmExplain
    bash concat_explain.sh $i          # Concatenate GkmExplain Scores
done

python nrkmers.py 11 /mnt/lab_data3/soumyak/adpd/kmer_scores/all-11mers.fa  # Get all non-redundant 11-mers

python schedule_kmers.py 1 24 40        # Run gkmpredict on all 11-mers

python run_deltasvm.py          # Run deltaSVM

