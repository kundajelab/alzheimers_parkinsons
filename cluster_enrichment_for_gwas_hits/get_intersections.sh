for cur_file in idr_peaks_bedtools_merged/*narrowPeak
do
    echo $cur_file
    cur_file_base=`basename $cur_file`
    bedtools intersect -u -wa -a Kunkle.1e-5.expanded.bed -b $cur_file > intersection.Kunkle.idr.clusters.$cur_file_base
    bedtools intersect -u -wa -a 23andme.1e-5.expanded.bed -b $cur_file > intersection.23andme.idr.clusters.$cur_file_base
done

for cur_file in overlap_peaks_bedtools_merged/*narrowPeak
do
    echo $cur_file
    cur_file_base=`basename $cur_file`
    bedtools intersect -u -wa -a Kunkle.1e-5.expanded.bed -b $cur_file > intersection.Kunkle.overlap.clusters.$cur_file_base
    bedtools intersect -u -wa -a 23andme.1e-5.expanded.bed -b $cur_file > intersection.23andme.overlap.clusters.$cur_file_base
done

for cur_file in celltype_idr_peaks_bedtools_merged/*narrowPeak
do
    echo $cur_file
    cur_file_base=`basename $cur_file`
    bedtools intersect -u -wa -a Kunkle.1e-5.expanded.bed -b $cur_file > celltype.intersection.Kunkle.idr.clusters.$cur_file_base
    bedtools intersect -u -wa -a 23andme.1e-5.expanded.bed -b $cur_file > celltype.intersection.23andme.idr.clusters.$cur_file_base
done

for cur_file in celltype_overlap_peaks_bedtools_merged/*narrowPeak
do
    echo $cur_file
    cur_file_base=`basename $cur_file`
    bedtools intersect -u -wa -a Kunkle.1e-5.expanded.bed -b $cur_file > celltype.intersection.Kunkle.overlap.clusters.$cur_file_base
    bedtools intersect -u -wa -a 23andme.1e-5.expanded.bed -b $cur_file > celltype.intersection.23andme.overlap.clusters.$cur_file_base
done
