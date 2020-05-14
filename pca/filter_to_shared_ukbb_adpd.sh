#!/bin/bash
#extract set of shared snps between adpd & 1kg
module load plink/1.90
plink --bfile merged.chr1 --extract shared.snps --make-bed --out merged.chr1.shared
plink --bfile 1000g.Phase3.chr1.maf0.05 --extract shared.snps --make-bed --out 1000g.Phase3.chr1.maf0.05.shared


