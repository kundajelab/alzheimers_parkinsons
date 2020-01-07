#!/bin/bash
for snp in `cat $1`
do
    zgrep -m1 -w $snp /mnt/data/annotations/dbSNP/common_all_20180418.vcf.gz >> hits &
done
