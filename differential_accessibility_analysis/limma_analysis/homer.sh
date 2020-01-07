#!/bin/bash

#for x in expanded_sva_diff_*

#do

    cut -f1,2,5 $1 | awk -F '\t' '{ if ($2 > 0) { print } }' | sort -k3,3n | head -n 10001 | cut -f1 | sed --expression "s/\_/\t/g" | grep -v "log" | bedtools sort -i stdin > ${1}_up.bed
    cut -f1,2,5 $1 | awk -F '\t' '{ if ($2 < 0) { print } }' | sort -k3,3n | head -n 10000 | cut -f1 | sed --expression "s/\_/\t/g" | grep -v "log" | bedtools sort -i stdin > ${1}_down.bed

#done
