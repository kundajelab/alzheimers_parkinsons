#!/bin/bash
#get a merged peak file                                                                                                                                                                                            
export prefix=idr
for region in `cat regions.txt`
do
    for peak_file in `cat $region`
    do
	zcat $peak_file >> $region.cat.bed
	echo -e "\n" >> $region.cat.bed
    done
    echo "concatenated peaks for region"
    #truncate peaks to 200 bp around summit
    python truncate_merged_peak_file_to_200bp_around_summit.py --input_bed $region.cat.bed --summit_flank 100 --outf $region.cat.200.bed
    bedtools sort -i $region.cat.200.bed > $region.cat.200.sorted.bed
    bedtools merge -i $region.cat.200.sorted.bed > $region.cat.200.sorted.merged.bed
    gzip $region.cat.200.sorted.merged.bed
    echo "generated merged peak file for region $region"
done
