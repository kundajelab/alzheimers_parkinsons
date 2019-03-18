#!/bin/bash
PROJECT_ROOT=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/
RUN_ROOT=$PROJECT_ROOT/outputs_PD
LOG_DIR=$RUN_ROOT/logs
mkdir -p $LOG_DIR

SH_SCRIPT=/scratch/groups/akundaje/annashch/testing/template_submission.sh

for type in $PROJECT_ROOT/PD/*; do
    for region in  $type/*; do
        for file in $region/*; do
	    type=$(basename $type)
	    region=$(basename $region)
	    prefix=$(basename $file .json)
	    WORK_DIR=$RUN_ROOT/$type/$region/$prefix
	    echo $WORK_DIR
	    mkdir -p $WORK_DIR && cd $WORK_DIR
	    ln -s $file
	    sbatch --partition akundaje --mem=30G \
		-o $LOG_DIR/$prefix.o -e $LOG_DIR/$prefix.e \
		-n 1 --ntasks-per-node=1 --partition akundaje,owners,normal --job-name=PD_ATAC --time=24:00:00 --cpus-per-task=2 --mail-type=END,FAIL \
		$SH_SCRIPT $file
        done
    done
done
