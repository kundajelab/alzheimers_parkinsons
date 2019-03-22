paste counts.*.txt > adpd.atac.counts.txt
#clean up temporary files                                                                                                                                                                                          

echo -e $'chrom\tstart\tend' > index
cat index naive_overlap.optimal_set.sorted.merged.bed > tmp1
paste tmp1 adpd.atac.counts.txt > tmp2
mv tmp2 adpd.atac.counts.txt

#clean up
rm tmp1
rm index
#rm counts.*.txt
