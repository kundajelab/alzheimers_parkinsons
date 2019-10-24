#!/bin/bash

for i in {1..24}
    do
        echo "Cluster "$i
        python expand_ld.py --snp_file /mnt/lab_data3/soumyak/adpd/snp_lists/Kunkle/Cluster$i.overlap.snps.hg19.bed --outf /mnt/lab_data3/soumyak/adpd/snp_lists/Kunkle/expanded/Cluster$i.overlap.expanded.snps.hg19.bed
    done

