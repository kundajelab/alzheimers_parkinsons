#!/bin/bash
for i in `seq 0 170`
do
    python get_seqs.py --variant_bed x$i --out_prefix dopa.variant.$i --fasta_ref /oak/stanford/groups/akundaje/refs/hg38/seq/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta
    echo $i 
done
