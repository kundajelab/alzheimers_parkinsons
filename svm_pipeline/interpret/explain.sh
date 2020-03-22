#!/bin/bash
input_index=$1
effect_or_noneffect=$2
model_split=$3

prefix=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/gkmexplain
gkmexplain $prefix/inputs_to_gkmexplain/dopa.variant.$input.effect.fa $prefix/models/model.DopaNeuronsCluster10.$model_split.model.txt $prefix/outputs_from_gkmexplain/gkmexplain.$input_index.$effect_or_noneffect.$model_split.txt

