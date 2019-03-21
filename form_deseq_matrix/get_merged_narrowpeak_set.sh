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
