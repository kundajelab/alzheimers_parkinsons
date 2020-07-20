#!/bin/bash

bash make_dirs.sh   # Make all directories for SVM SNP scoring

python get_null_seqs.py         # Get null input sequences

python schedule_ism.py 1 24 40  # Run gkmpredict for ISM scores

bash get_ism_scores.sh          # Get ISM scores

for i in {1..24}
do
    python schedule_gkmexplain.sh $i   # Run GkmExplain
    bash concat_explain.sh $i          # Concatenate GkmExplain Scores
done

python run_deltasvm.py          # Run deltaSVM

