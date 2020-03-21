task=$1
idr=$2
python get_svm_peak_splits.py \
       --narrowPeak $idr \
       --ntrain 60000 \
       --out_prefix $task.svm.peaks \
       --genome hg38
