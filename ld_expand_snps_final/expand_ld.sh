#!/bin/bash
#python expand_ld.py --snp_pos_bed_file snps.hg19.bed --outf snps.hg19.bed.expanded

#split by gwas source
for f in *formatted*
do
    python expand_ld.py --snp_pos_bed_file $f --outf ld.expanded.$f
done
    
