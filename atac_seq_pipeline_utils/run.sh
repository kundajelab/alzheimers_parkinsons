#!/bin/bash
PROJECT_ROOT=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/
RUN_ROOT=$PROJECT_ROOT/outputs
LOG_DIR=$RUN_ROOT/logs
mkdir -p $LOG_DIR

DATA_ROOT=$PROJECT_ROOT/AD/ADAD
SH_SCRIPT=/scratch/groups/akundaje/annashch/testing/template_submission.sh

for type in $PROJECT_ROOT/AD/*; do
    for region in $type/*; do
        for file in $region/*; do
            prefix=$(basename $file .json)
            WORK_DIR=$RUN_ROOT/$type/$region/$prefix
            mkdir -p $WORK_DIR && cd $WORK_DIR
            ln -s $file
            sbatch --partition akundaje --mem=30G \
                -o $LOG_DIR/$prefix.o -e $LOG_DIR/$prefix.e \
                $SH_SCRIPT $file
        done
    done
done
