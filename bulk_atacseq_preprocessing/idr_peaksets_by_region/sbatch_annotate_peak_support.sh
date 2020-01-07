#!/bin/bash

#control regions 
for region in `cat controls/regions.txt`
do
    sbatch --partition akundaje,euan,owners,normal -o logs/CTRL.$region.o -e logs/CTRL.$region.e --job-name CTRL.$region annotate_peak_support.controls.sh $region 
done

#all regions 
#for region in `cat all/regions.txt`
#do
#    sbatch --partition akundaje,euan,owners,normal -o logs/ALL.$region.o -e logs/ALL.$region.e --job-name ALL.$region annotate_peak_support.all.sh $region 
#done
