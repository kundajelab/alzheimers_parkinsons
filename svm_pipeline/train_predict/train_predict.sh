#!/bin/bash
task=$1
fold=$2

#gkmtrain -m 10000 -v 2 -T 16 /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/svm_inputs/$task.svm.inputs.train.$fold.positives /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/svm_inputs/$task.svm.inputs.train.$fold.negatives /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/models/model.$task.$fold
gkmpredict -v 2 -T 16 /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/svm_inputs/$task.svm.inputs.test.$fold.positives /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/models/model.$task.$fold.model.txt /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/predictions/$task.$fold.positives
gkmpredict -v 2 -T 16 /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/svm_inputs/$task.svm.inputs.test.$fold.negatives /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/models/model.$task.$fold.model.txt /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/predictions/$task.$fold.negatives
