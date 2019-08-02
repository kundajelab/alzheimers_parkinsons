for cluster in `seq 1 24`
do    
    Rscript granges_to_tagAlign.R Cluster$cluster-fragments.rds Cluster$cluster.tagAlign.gz 99 &
done


