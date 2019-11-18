#get a merged peak file                                                                                                                                                                                            
rm naive_overlap.optimal_set.bed
rm naive_overlap.optimal_set.sorted.bed
rm naive_overlap.optimal_set.sorted.merged.bed

for peak_file in `cut -f2 narrowPeak.files.txt`
do
    zcat $peak_file >> naive_overlap.optimal_set.bed
done
#truncate peaks to 200 bp around summit
python truncate_merged_peak_file_to_200bp_around_summit.py --input_bed naive_overlap.optimal_set.bed --summit_flank 100 --outf naive_overlap.optimal_set.200.bed
bedtools sort -i naive_overlap.optimal_set.200.bed > naive_overlap.optimal_set.sorted.bed
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

echo -e $'chrom\tstart\tend' > index
cat index naive_overlap.optimal_set.sorted.merged.bed > tmp1
paste tmp1 adpd.atac.counts.txt > tmp2
mv tmp2 adpd.pseudobulk.overlap.atac.counts.txt

#clean up
rm tmp1
rm index
#rm counts.*.txt
