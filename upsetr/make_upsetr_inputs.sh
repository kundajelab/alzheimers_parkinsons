#PD
python make_upsetr_inputs.py --limma_diff_peaks ../limma_analysis/diff_pd_* --outf PD.NOSVA.TypeModRegionMod.upsetr.input.tsv
python make_upsetr_inputs.py --limma_diff_peaks ../limma_analysis/expanded_diff_pd_* --outf PD.NOSVA.TypeRegion.upsetr.inputs.tsv
python make_upsetr_inputs.py --limma_diff_peaks ../limma_analysis/sva_diff_pd_* --outf PD.SVA.TypeModRegionMod.upsetr.inputs.tsv
python make_upsetr_inputs.py --limma_diff_peaks ../limma_analysis/expanded_sva_diff_pd_* --outf PD.SVA.TypeRegion.upsetr.inputs.tsv

#AD
python make_upsetr_inputs.py --limma_diff_peaks /users/soumyak/alzheimers_parkinsons/limma_analysis/no_sva_typemod/diff*tsv --outf AD.NOSVA.TypeModRegionMod.upsetr.inputs.tsv
python make_upsetr_inputs.py --limma_diff_peaks /users/soumyak/alzheimers_parkinsons/limma_analysis/no_sva_expanded/expanded_*tsv --outf AD.NOSVA.TypeRegion.upsetr.inputs.tsv
python make_upsetr_inputs.py --limma_diff_peaks /users/soumyak/alzheimers_parkinsons/limma_analysis/sva_expanded/expanded_sva_*tsv --outf AD.SVA.TypeRegion.upsetr.inputs.tsv
python make_upsetr_inputs.py --limma_diff_peaks /users/soumyak/alzheimers_parkinsons/limma_analysis/sva_typemod/sva_*tsv --outf AD.SVA.TypeModRegionMod.upsetr.inputs.tsv
