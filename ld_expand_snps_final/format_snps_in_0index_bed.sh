prefix="/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/snps_final/gwas_specific_191023_All_GWAS_SNPs_unique"
for gwas_source in $prefix/*.snps
do
    outf=`basename $gwas_source`'.formatted'
    python format_snps_in_0index_bed.py --i $gwas_source --o $outf
    outf_gwas=`basename $gwas_source`'.formatted.gwas'
    python format_snps_in_0index_bed.py --i $gwas_source.gwas --o $outf_gwas
done
