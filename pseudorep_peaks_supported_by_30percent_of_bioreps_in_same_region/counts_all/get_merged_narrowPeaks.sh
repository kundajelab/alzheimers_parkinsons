#!/bin/bash
#get a merged peak file                                                                                                                                                                                            
export prefix=idr
#prefix=naive_overlap 

#rm $prefix.optimal_set.bed
#rm $prefix.optimal_set.sorted.bed
#rm $prefix.optimal_set.sorted.merged.bed

for peak_file in `cut -f2 optimal.$prefix.narrowPeaks.txt`
do
    zcat $peak_file >> $prefix.optimal_set.bed
    echo -e "\n" >> $prefix.optimal_set.bed 
done

#truncate peaks to 200 bp around summit
python truncate_merged_peak_file_to_200bp_around_summit.py --input_bed $prefix.optimal_set.bed --summit_flank 100 --outf $prefix.optimal_set.200.bed
bedtools sort -i $prefix.optimal_set.200.bed > $prefix.optimal_set.sorted.bed
bedtools merge -i $prefix.optimal_set.sorted.bed > $prefix.optimal_set.sorted.merged.bed
echo "generated merged peak file!"
