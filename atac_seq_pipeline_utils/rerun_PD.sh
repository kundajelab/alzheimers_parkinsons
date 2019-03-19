#!/bin/bash
PROJECT_ROOT=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/
RUN_ROOT=$PROJECT_ROOT/outputs_PD
LOG_DIR=$RUN_ROOT/logs
mkdir -p $LOG_DIR

SH_SCRIPT=/scratch/groups/akundaje/annashch/alzheimers_parkinsons/atac_seq_pipeline_utils/template_submission.sh
TO_RERUN=to_rerun_PD.txt
for file in `cat $TO_RERUN`; do
    prefix=$(basename $file .json)
    region_folder=$(dirname $file) 
    region=$(basename $region_folder) 
    type_folder=$(dirname $region_folder) 
    type=$(basename $type_folder) 
    WORK_DIR=$RUN_ROOT/$type/$region/$prefix
    echo $WORK_DIR
    cd $WORK_DIR
    sbatch --partition akundaje,euan --mem=50G \
	-o $LOG_DIR/$prefix.o -e $LOG_DIR/$prefix.e \
	-n 1 --ntasks-per-node=1  --job-name=$file --time=24:00:00 --cpus-per-task=2 \
	$SH_SCRIPT $file
done
