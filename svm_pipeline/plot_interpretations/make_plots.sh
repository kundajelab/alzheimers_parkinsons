#!/bin/bash
gkmexplain_prefix=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/gkmexplain/outputs_from_gkmexplain/gkmexplain.
outf_prefix=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/gkmexplain_plots
for fold in `seq 0 9`
do
    
    python make_plots.py --snpinfo toplot.txt \
	   --gkmexplain_prefix $gkmexplain_prefix \
	   --gkmexplain_suffix .txt \
	   --fold $fold \
	   --outf_prefix $outf_prefix \
	   --flank 500 \
	   --plot_start_base 400 \
	   --plot_end_base 600 \
	   --snp_pos 501
done

