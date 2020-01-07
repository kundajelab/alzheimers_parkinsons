#rGREAT can only handle 1 million regions in the background set, we collapse the background in a cluster-specific way to accommodate this limit.
for cluster in `seq 1 24`
do
    bedtools intersect -v -a overlap.background.sorted.bed -b Cluster$cluster.bed | bedtools merge -i stdin > tmp
    cat Cluster$cluster.bed tmp > background.Cluster$cluster.bed
    rm tmp
    echo $cluster
done
