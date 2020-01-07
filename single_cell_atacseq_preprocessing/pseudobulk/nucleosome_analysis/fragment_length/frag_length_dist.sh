for cluster in `seq 1 24`
do    
    Rscript frag_length_dist.R /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_rds/Cluster$cluster-fragments.rds Cluster$cluster.fraglen.gz &
done
