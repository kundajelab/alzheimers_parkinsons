#!/bin/bash
inputf=$1
num_snps=`cat $inputf| wc -l`
echo $num_snps 
for ((i=1;i<=num_snps;i++)); do
    cur_snp=`cut -f1 $inputf | head -n $i | tail -n1`
    cur_cluster=`cut -f2 $inputf | head -n $i | tail -n1`
    cur_fold=`cut -f3 $inputf | head -n $i | tail -n1`
    cur_effect=`cut -f4 $inputf| head -n $i | tail -n1`
    cur_noneffect=`cut -f5 $inputf| head -n $i | tail -n1`
    echo "snp:$cur_snp"
    echo "cluster:$cur_cluster"
    echo "fold:$cur_fold"
    echo "effect:$cur_effect"
    echo "noneffect:$cur_noneffect" 
    python plot_folds.py --cluster $cur_cluster --test_fold $cur_fold --snp $cur_snp --effect_allele $cur_effect --noneffect_allele $cur_noneffect 
done
