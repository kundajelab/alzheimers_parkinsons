#!/bin/bash 
prefix_in=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/gkmexplain/outputs_from_gkmexplain/parts
prefix_out=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/gkmexplain/outputs_from_gkmexplain/
for index in `seq 0 169`
do
    echo $index
    for split in `seq 0 9` 
    do
	echo $split
	for effect in effect noneffect 
	do
	    cat $prefix_in/gkmexplain.$index.$effect.$split.txt >> $prefix_out/gkmexplain.$effect.$split.txt 
	done
    done
done
