task=$1
ref=$2
python form_svm_input_fastas.py --outf $task.svm.inputs.test.0 $task.svm.inputs.test.1 $task.svm.inputs.test.2 $task.svm.inputs.test.3 $task.svm.inputs.test.4 $task.svm.inputs.test.5 $task.svm.inputs.test.6 $task.svm.inputs.test.7 $task.svm.inputs.test.8 $task.svm.inputs.test.9 $task.svm.inputs.train.0 $task.svm.inputs.train.1 $task.svm.inputs.train.2 $task.svm.inputs.train.3 $task.svm.inputs.train.4 $task.svm.inputs.train.5 $task.svm.inputs.train.6 $task.svm.inputs.train.7 $task.svm.inputs.train.8 $task.svm.inputs.train.9 \
       --neg_pickle $task.candidate.negatives.gc.p \
       --overwrite_outf \
       --ref_fasta $ref \
       --peaks $task.svm.peaks.test.0.gc.seq $task.svm.peaks.test.1.gc.seq $task.svm.peaks.test.2.gc.seq $task.svm.peaks.test.3.gc.seq $task.svm.peaks.test.4.gc.seq $task.svm.peaks.test.5.gc.seq $task.svm.peaks.test.6.gc.seq $task.svm.peaks.test.7.gc.seq $task.svm.peaks.test.8.gc.seq $task.svm.peaks.test.9.gc.seq $task.svm.peaks.train.0.gc.seq $task.svm.peaks.train.1.gc.seq $task.svm.peaks.train.2.gc.seq $task.svm.peaks.train.3.gc.seq $task.svm.peaks.train.4.gc.seq $task.svm.peaks.train.5.gc.seq $task.svm.peaks.train.6.gc.seq $task.svm.peaks.train.7.gc.seq $task.svm.peaks.train.8.gc.seq $task.svm.peaks.train.9.gc.seq
