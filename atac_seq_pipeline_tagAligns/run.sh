#!/bin/bash
RUN_ROOT=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/merged_tagAligns_outputs
LOG_DIR=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/merged_tagAligns_outputs/logs 
mkdir -p $LOG_DIR

SH_SCRIPT=/scratch/PI/akundaje/annashch/alzheimers_parkinsons/atac_seq_pipeline_tagAligns/template_submission.sh
for sample in `cat input_jsons.txt`
do
    echo $sample
    sample_dir=`dirname $sample`
    sample_name=`basename $sample`
    cd $sample_dir
    sbatch --partition akundaje,owners,euan,normal \
	--mem=50G \
	-o $LOG_DIR/$sample_name.o \
	-e $LOG_DIR/$sample_name.e  \
	-n 1 \
	--ntasks-per-node=1 \
	--job-name=$sample_name \
	-t 2-0 \
	--cpus-per-task=4 \
	$SH_SCRIPT $sample_name
done
