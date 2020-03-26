#!/bin/bash
#task_order: dnase_c dnase_v sw480 hct116 colo205 
gkmexplain_prefix=/oak/stanford/groups/akundaje/projects/GECCO/SVM/gkmexplain_scores/aggregate_nodups/scores
deepshap_prefix=/srv/scratch/annashch/gecco/interpret_cnn/deepshap
outf_prefix=/srv/scratch/annashch/gecco/plots
python plot_folds.py --snpinfo toplot.txt \
       --tasks dnase_c dnase_v sw480 hct116 colo205 \
       --gkmexplain_prefix $gkmexplain_prefix \
       --gkmexplain_suffix .txt.filtered \
       --deepshap_pickle_classification_prefix $deepshap_prefix/deepshap.classification. \
       --deepshap_pickle_regression_prefix $deepshap_prefix/deepshap.regression. \
       --outf_prefix $outf_prefix \
       --plot_start_base 400 \
       --plot_end_base 600 \
       --snp_pos 501

