#thresholded
python create_gwas_bed_files.py --gwas mgloud_GWAS/GWAS_Kunkle2019.txt.gz --out_prefix Kunkle.1e-5 --append --pval_thresh 1e-5
python create_gwas_bed_files.py --gwas mgloud_GWAS/23andme_PD.txt.gz --out_prefix 23andme.1e-5 --pval_thresh 1e-5
#not thresholded
python create_gwas_bed_files.py --gwas mgloud_GWAS/GWAS_Kunkle2019.txt.gz --out_prefix Kunkle --append 
python create_gwas_bed_files.py --gwas mgloud_GWAS/23andme_PD.txt.gz --out_prefix 23andme 


