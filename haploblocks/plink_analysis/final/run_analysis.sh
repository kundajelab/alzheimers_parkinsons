##get haploblocks 
plink --bfile chr17_phase3_bed_range  --blocks-max-kb 2000 --blocks no-pheno-req
##get haploblock frequencies 
../../plink-1.04-x86_64/plink --bfile chr17_phase3_bed_range --hap plink.blocks --hap-freq --noweb

