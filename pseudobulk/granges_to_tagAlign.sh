for cluster in `seq 1 24`
do    
    Rscript granges_to_tagAlign.R /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_rds/Cluster$cluster-fragments.rds /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_tagAligns/clusters/Cluster$cluster.tagAlign.gz 99 &
done


