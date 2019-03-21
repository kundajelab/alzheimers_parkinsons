#get a merged peak file                                                                                                                                                                                            
rm naive_overlap.optimal_set.bed
rm naive_overlap.optimal_set.sorted.bed
rm naive_overlap.optimal_set.sorted.merged.bed

for peak_file in `cut -f2 narrowPeak.files.txt`
do
    zcat $peak_file >> naive_overlap.optimal_set.bed
done
bedtools sort -i naive_overlap.optimal_set.bed > naive_overlap.optimal_set.sorted.bed
bedtools merge -i naive_overlap.optimal_set.sorted.bed > naive_overlap.optimal_set.sorted.merged.bed

echo "generated merged peak file!"

#get the counts for each sample within each peak                                                                                                                                                                   
export numfiles=`cat tagAlign.files.txt | wc -l`
echo $numfiles
for i in $(seq 1 $numfiles)
do
    cur_sample_name=`head -n $i tagAlign.files.txt | tail -n1 | cut -f1`
    echo $cur_sample_name > counts.$cur_sample_name.txt
    cur_tagalign=`head -n $i tagAlign.files.txt | tail -n1 | cut -f2`
    echo $cur_sample_name
    bedtools coverage -counts -a naive_overlap.optimal_set.sorted.merged.bed -b $cur_tagalign | cut -f4 >> counts.$cur_sample_name.txt
done
paste counts.*.txt > adpd.atac.counts.txt
#clean up temporary files                                                                                                                                                                                          
rm counts.*.txt
paste naive_overlap.optimal_set.sorted.merged.bed adpd.atac.counts.txt > tmp
mv tmp adpd.atac.counts.txt
