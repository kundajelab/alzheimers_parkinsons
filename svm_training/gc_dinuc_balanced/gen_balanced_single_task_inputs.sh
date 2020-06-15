python gen_balanced_single_task_inputs.py --train_all_labels /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/gecco_v2.train.bed \
       --valid_all_labels /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/gecco_v2.validate.bed \
       --test_all_labels /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/gecco_v2.test.bed \
       --task_subset_prefix /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/train \
       --task_subset_suffix npy \
       --out_prefix single
