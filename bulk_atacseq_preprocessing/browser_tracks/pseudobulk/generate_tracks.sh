prefix=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs
python generate_tracks.py --pval_bigwigs $prefix/pval.signal.bigwig \
    --fc_bigwigs $prefix/fc.signal.bigwig  \
    --hammocks $prefix/idr.optimal.narrowPeak.hammock.txt \
    --outf_fc_bigwig $prefix/adpd_fc_bigwig.json \
    --outf_pval_bigwig $prefix/adpd_pval_bigwig.json \
    --mitra_prefix http://mitra.stanford.edu/kundaje/projects/alzheimers_parkinsons \
    --prefix_to_drop_for_oak /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons





