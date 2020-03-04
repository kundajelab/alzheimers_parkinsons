#!/bin/bash

samtools mpileup -f /home/groups/cherry/encode/pipeline_genome_data/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta -t DP,DP4 -v $1
