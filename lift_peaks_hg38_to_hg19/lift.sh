#celltype peaks 
prefix=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs_celltypes/peaks
for cluster in $prefix/overlap_peaks_bedtools_merged/*narrowPeak
do
    base_cluster=`basename $cluster`
    echo $base_cluster 
    liftOver $cluster hg38ToHg19.over.chain.gz $prefix/hg19_overlap_peaks_bedtools_merged/$base_cluster $prefix/hg19_overlap_peaks_bedtools_merged/$base_cluster.unlifted
done

for cluster in $prefix/idr_peaks_bedtools_merged/*narrowPeak
do
    base_cluster=`basename $cluster`
    echo $base_cluster 
    liftOver $cluster hg38ToHg19.over.chain.gz $prefix/hg19_idr_peaks_bedtools_merged/$base_cluster $prefix/hg19_overlap_peaks_bedtools_merged/$base_cluster.unlifted
done

#cluster peaks
prefix=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks
for cluster in $prefix/overlap_peaks_bedtools_merged/*narrowPeak
do
    base_cluster=`basename $cluster`
    echo $base_cluster 
    liftOver $cluster hg38ToHg19.over.chain.gz $prefix/hg19_overlap_peaks_bedtools_merged/$base_cluster $prefix/hg19_overlap_peaks_bedtools_merged/$base_cluster.unlifted
done

for cluster in $prefix/idr_peaks_bedtools_merged/*narrowPeak
do
    base_cluster=`basename $cluster`
    echo $base_cluster 
    liftOver $cluster hg38ToHg19.over.chain.gz $prefix/hg19_idr_peaks_bedtools_merged/$base_cluster $prefix/hg19_overlap_peaks_bedtools_merged/$base_cluster.unlifted
done
