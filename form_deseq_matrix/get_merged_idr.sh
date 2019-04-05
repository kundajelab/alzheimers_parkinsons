#!/bin/bash
#get a merged peak file                                                                                                                                                                                            
#rm idr.optimal_set.bed
#rm idr.optimal_set.sorted.bed
#rm idr.optimal_set.sorted.merged.bed

for peak_file in `cut -f2 optimal.idr.narrowPeaks.txt`
do
    zcat $peak_file >> idr.optimal_set.bed
done

#truncate peaks to 200 bp around summit
python truncate_merged_peak_file_to_200bp_around_summit.py --input_bed idr.optimal_set.bed --summit_flank 100 --outf idr.optimal_set.200.bed
bedtools sort -i idr.optimal_set.200.bed > idr.optimal_set.sorted.bed
bedtools merge -i idr.optimal_set.sorted.bed > idr.optimal_set.sorted.merged.bed
echo "generated merged peak file!"
