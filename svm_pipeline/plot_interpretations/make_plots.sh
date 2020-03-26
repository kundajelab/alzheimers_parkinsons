#!/bin/bash
#task_order: dnase_c dnase_v sw480 hct116 colo205 
gkmexplain_prefix=/srv/scratch/annashch/gecco/gkmexplain/score_summary_and_significance/
deepshap_prefix=/srv/scratch/annashch/gecco/interpret_cnn/deepshap
outf_prefix=/srv/scratch/annashch/gecco/plots
python make_plots.py --snpinfo toplot.txt \
       --gkmexplain_pickle_prefix $gkmexplain_prefix \
       --gkmexplain_pickle_suffix .gkmexplain.aggregate.txt.intermediate.p \
       --deepshap_pickle_classification_prefix $deepshap_prefix/deepshap.classification. \
       --deepshap_pickle_regression_prefix $deepshap_prefix/deepshap.regression. \
       --outf_prefix $outf_prefix \
       --plot_start_base 400 \
       --plot_end_base 600 \
       --snp_pos 501

