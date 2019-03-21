#!/bin/bash
PROJECT_ROOT=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/
RUN_ROOT=$PROJECT_ROOT/outputs_PD
LOG_DIR=$RUN_ROOT/logs
mkdir -p $LOG_DIR

SH_SCRIPT=/scratch/groups/akundaje/annashch/alzheimers_parkinsons/atac_seq_pipeline_utils/template_submission.sh
TO_RERUN=resumer_files.txt
for file in `cat $TO_RERUN`; do
    WORK_DIR=$(dirname $file) 
    prefix=$(basename $WORK_DIR) 
    cd $WORK_DIR 
    echo $prefix
    sbatch --partition akundaje,euan,normal,owners --mem=50G \
	-o $LOG_DIR/$prefix.o -e $LOG_DIR/$prefix.e \
	-n 1 --ntasks-per-node=1  --job-name=$file --time=24:00:00 --cpus-per-task=2 \
	$SH_SCRIPT $file
done
