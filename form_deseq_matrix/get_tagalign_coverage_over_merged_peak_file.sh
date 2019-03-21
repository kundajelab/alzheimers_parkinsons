#!/bin/bash 
bedtools coverage -counts -a naive_overlap.optimal_set.sorted.merged.bed -b $1 | cut -f4 >> counts.$2.txt
