## by re-coded snp coordinates
plink --bfile chr17_phase3_bed --extract range ../hg19_coords.csv --make-bed --out chr17_phase3_bed_range
## by range 
#plink --bfile chr17_phase3_bed --extract range ../range.txt --make-bed --out chr17_phase3_bed_range
##by name
#plink --bfile chr17_phase3_bed --extract ../tokeep.txt --make-bed --out chr17_phase3_bed_subset
#plink --bfile 1kg_phase1_chr17 --extract tokeep.txt --make-bed --out 1kg_phase1_chr17_subset
