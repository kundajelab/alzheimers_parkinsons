export prefix=idr #or naive_overlap 
paste counts.*.txt > pr.adpd.atac.$prefix.counts.txt
#clean up temporary files                                                                                                                                                                                          

echo -e $'chrom\tstart\tend' > index
cat index $prefix.optimal_set.sorted.merged.bed > tmp1
paste tmp1 pr.adpd.atac.$prefix.counts.txt > tmp2
mv tmp2 pr.adpd.atac.$prefix.counts.txt

#clean up
rm tmp1
rm index
#rm counts.*.txt
