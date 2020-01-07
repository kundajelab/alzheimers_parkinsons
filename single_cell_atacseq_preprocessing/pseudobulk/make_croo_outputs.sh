#!/bin/bash
hash_log=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/hash_to_sample.txt
num_rows=`cat $hash_log | wc -l`
#print($num_rows)
for i in $(seq 1 $num_rows)
do
    cur_hash=`head -n $i $hash_log | tail -n1 | cut -f1`
    cur_experiment=`head -n $i $hash_log | tail -n1 | cut -f2`
    echo $cur_hash
    echo $cur_experiment
    croo /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/atac/$cur_hash/metadata.json  --out-dir /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/croo_outputs/$cur_experiment --use-rel-path-in-link
    #symlink the qc report in croo output dir
    ln -s /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/atac/$cur_hash/call-qc_report/execution/qc.html  /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/croo_outputs/$cur_experiment/$cur_experiment.qc.html
done
