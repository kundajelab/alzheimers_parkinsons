#!/bin/bash

R --vanilla --args /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allelic_imbalance/quasar/pileup_bed/${1}.pileup.bed.gz < /home/groups/akundaje/soumyak/QuASAR/scripts/convertPileupToQuasar.R

