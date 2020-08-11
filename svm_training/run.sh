#!/bin/bash

bash make_dirs.sh   # Make all directories for SVM model training

python generate_tasks_sc.py     # Make input task file for seqdataloader

python get_gkmsvm_inputs.py     # Run seqdataloader to get input labels

python get_gkmsvm_positives.py  # Get positive training examples

python get_gkmsvm_negatives.py  # Get negative training examples

python schedule_gkmsvm.py 1 24  # Train gkm-SVM models and get accuracy

