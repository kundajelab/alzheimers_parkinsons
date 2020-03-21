task=DopaNeuronsCluster10
idr=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/croo/peak/idr_reproducibility/idr.optimal_peak.narrowPeak.gz #COLL.idr.optimal_peak.narrowPeak.summits.max.signale
ref=/mnt/data/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta
#echo "starting $task $idr" 
#./get_svm_peak_splits.sh $task $idr
#echo "got svm peak splits" 
#./get_gc_positives.sh $task
#echo "got gc content of the positive sequences" 
#./get_all_negatives.sh $task $idr
#echo "got candidate negative set" 
#./get_chrom_gc_region_dict.sh $task
#echo "created python pickle for candidate negatives" 
./form_svm_input_fastas.sh $task $ref
#echo "finished creating SVM inputs" 

 
