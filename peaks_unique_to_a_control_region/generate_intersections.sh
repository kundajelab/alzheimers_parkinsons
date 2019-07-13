#!/bin/bash 

#give bed file of peaks in region as input 
numsamples=`cat $1 | wc -l`
for i in $(seq 1 $numsamples)
do
    cur_sample_name=`head -n $i $1 | tail -n1 | cut -f1`
    echo $cur_sample_name 
    cur_sample=`head -n $i $1 | tail -n1 | cut -f2`
    echo $cur_sample
    bedtools intersect -wa -a ctr.idr.optimal_set.sorted.merged.bed  -b $cur_sample  | cut -f1,2,3 | sort |uniq  > $cur_sample_name.intersection.bed 
done
