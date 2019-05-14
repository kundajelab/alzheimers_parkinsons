#!/bin/bash
#get a merged peak file                                                                                                                                                                                            
export prefix=idr
for region in `cat regions.txt`
do
    for peak_file in `cat $region.ctr.optimal.$prefix.narrowPeak.txt`
    do
	zcat $peak_file >> $region.ctr.$prefix.optimal_set.bed
    done
    #truncate peaks to 200 bp around summit
    python truncate_merged_peak_file_to_200bp_around_summit.py --input_bed $region.ctr.$prefix.optimal_set.bed --summit_flank 100 --outf $region.ctr.$prefix.optimal_set.200.bed
    bedtools sort -i $region.ctr.$prefix.optimal_set.200.bed > $region.ctr.$prefix.optimal_set.sorted.bed
    bedtools merge -i $region.ctr.$prefix.optimal_set.sorted.bed > $region.ctr.$prefix.optimal_set.sorted.merged.bed
    echo "generated merged peak file for region $region"
done
