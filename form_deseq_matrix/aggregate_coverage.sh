paste counts.*.txt > adpd.atac.counts.txt
#clean up temporary files                                                                                                                                                                                          
rm counts.*.txt
paste naive_overlap.optimal_set.sorted.merged.bed adpd.atac.counts.txt > tmp
mv tmp adpd.atac.counts.txt
