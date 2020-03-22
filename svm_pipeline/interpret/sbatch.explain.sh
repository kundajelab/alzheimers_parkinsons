for input_index in `seq 0 169`
do
    for effect_or_noneffect in effect noneffect 
    do
	for model_split in `seq 0 9` 
	do
	    sbatch -J $input_index.$effect_or_noneffect.$model_split -o logs/$input_index.$effect_or_noneffect.$model_split.o -e logs/$input_index.$effect_or_noneffect.$model_split.e -p akundaje,euan,owners,normal --time=1440 ./explain.sh $input_index $effect_or_noneffect $model_split 
	done
    done
done
