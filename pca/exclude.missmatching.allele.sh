#!/bin/bash
plink --bfile merged.chr1.shared --exclude common-merge.missnp --make-bed --out merged.chr1.shared.nomismatch
plink --bfile 1000g.Phase3.chr1.maf0.05.shared --exclude common-merge.missnp --make-bed --out 1000g.Phase3.chr1.maf0.05.shared.nomismatch

