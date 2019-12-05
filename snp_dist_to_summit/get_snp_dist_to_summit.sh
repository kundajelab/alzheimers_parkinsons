python get_snp_dist_to_summit.py --peak_prefix /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/idr_peaks/Cluster \
       --peak_suffix .idr.optimal.narrowPeak \
       --snps snps.bed \
       --nclusters 24 \
       --outf snp_summit_dist.idr.txt
python get_snp_dist_to_summit.py --peak_prefix /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/overlap_peaks/Cluster \
       --peak_suffix .overlap.optimal.narrowPeak \
       --snps snps.bed \
       --nclusters 24 \
       --outf snp_summit_dist.overlap.txt

