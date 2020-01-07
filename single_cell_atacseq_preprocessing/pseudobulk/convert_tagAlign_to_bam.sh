for cluster in 1 #`seq 1 24`
do

    bedToBam -i /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_tagAligns/clusters/Cluster$cluster.tagAlign.gz -g /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/hg38.chrom.sizes >  /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseubobulk_bam/Cluster$cluster.bam 
done

