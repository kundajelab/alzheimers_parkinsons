for task in dnase_c dnase_v colo205 sw480 hct116
do
    for fold in `seq 0 9`
    do
	python get_auprc.py $task $fold  >> /srv/scratch/annashch/gecco/SVM/perf.svm.svmtrainset.genometestset/perf.metrics.txt.$task.$fold &
	echo "$task $fold"
    done
done
