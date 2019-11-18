
#aggregates pseudobulk tagAligns to cell types
#Cluster13   Astrocytes
#Cluster14   Astrocytes
#Cluster15   Astrocytes
#Cluster16   Astrocytes
#Cluster17   Astrocytes
#Cluster1    Excitatory Neurons
#Cluster3    Excitatory Neurons
#Cluster4    Excitatory Neurons
#Cluster11   Inhibitory Neurons
#Cluster12   Inhibitory Neurons
#Cluster2    Inhibitory Neurons
#Cluster24   Microglia
#Cluster19   Oligodendrocytes
#Cluster20   Oligodendrocytes
#Cluster21   Oligodendrocytes
#Cluster22   Oligodendrocytes
#Cluster23   Oligodendrocytes
#Cluster10   OPCs
#Cluster8    OPCs
#Cluster9    OPCs
#Cluster5    Nigral Neurons
#Cluster6    Nigral Neurons
#Cluster18   Doublets
#Cluster7    Neurons - Unknown

prefix=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_tagAligns/
cat $prefix/clusters/Cluster13.tagAlign.gz $prefix/clusters/Cluster14.tagAlign.gz $prefix/clusters/Cluster15.tagAlign.gz $prefix/clusters/Cluster16.tagAlign.gz $prefix/clusters/Cluster17.tagAlign.gz > $prefix/celltypes/astrocytes.tagAlign.gz
cat $prefix/clusters/Cluster1.tagAlign.gz $prefix/clusters/Cluster3.tagAlign.gz $prefix/clusters/Cluster4.tagAlign.gz > $prefix/celltypes/excitatory_neurons.tagAlign.gz
cat $prefix/clusters/Cluster11.tagAlign.gz $prefix/clusters/Cluster12.tagAlign.gz $prefix/clusters/Cluster2.tagAlign.gz > $prefix/celltypes/inhibitory_neurons.tagAlign.gz
cat $prefix/clusters/Cluster24.tagAlign.gz >$prefix/celltypes/micorglia.tagAlign.gz
cat $prefix/clusters/Cluster19.tagAlign.gz $prefix/clusters/Cluster20.tagAlign.gz $prefix/clusters/Cluster21.tagAlign.gz $prefix/clusters/Cluster22.tagAlign.gz $prefix/clusters/Cluster23.tagAlign.gz > $prefix/celltypes/oligodendrocytes.tagAlign.gz
cat $prefix/clusters/Cluster10.tagAlign.gz $prefix/clusters/Cluster8.tagAlign.gz $prefix/clusters/Cluster9.tagAlign.gz > $prefix/celltypes/opcs.tagAlign.gz
cat $prefix/clusters/Cluster5.tagAlign.gz $prefix/clusters/Cluster6.tagAlign.gz > $prefix/celltypes/nigral_neurons.tagAlign.gz
cat $prefix/clusters/Cluster18.tagAlign.gz > $prefix/celltypes/doublets.tagAlign.gz
cat $prefix/clusters/Cluster7.tagAlign.gz > $prefix/celltypes/neurons_unknown.tagAlign.gz

