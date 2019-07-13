#!/bin/bash
RUN_ROOT=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/merged_tagAligns_outputs
LOG_DIR=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/merged_tagAligns_outputs/logs 
TO_RERUN=/scratch/PI/akundaje/annashch/alzheimers_parkinsons/atac_seq_pipeline_tagAligns/resumer_files.txt
SH_SCRIPT=/scratch/PI/akundaje/annashch/alzheimers_parkinsons/atac_seq_pipeline_tagAligns/template_submission.sh
for file in `cat $TO_RERUN`; do
#for file in `cat tmp`; do
    WORK_DIR=$(dirname $file) 
    prefix=$(basename $WORK_DIR) 
    cd $WORK_DIR 
    echo $prefix
    sbatch --partition akundaje \
	--mem=65G \
	-o $LOG_DIR/$prefix.o \
	-e $LOG_DIR/$prefix.e \
	-n 1 \
	--ntasks-per-node=1  \
	--job-name=$file \
	-t 1-0 \
	--cpus-per-task=4 \
	$SH_SCRIPT $file
done
