#!/bin/bash
module load samtools
ref=/home/groups/akundaje/annashch/alzheimers_parkinsons/aux/mpileup/individual_bams/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta
prefix=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/
bcf_pileup_prefix=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/individual_bams/mpileup_output
numfiles=`cat $prefix/bams.txt| wc -l`
for i in 192 248 400 #`seq 1 $numfiles`
do
    cur_bam=`head -n $i $prefix/bams.txt | tail -n1` 
    echo $cur_bam 
    cur_name=`head -n $i $prefix/bam_names.txt | tail -n1`
    echo $cur_name
    outf=$bcf_pileup_prefix/$cur_name.bcf.gz
    sbatch -J mpileup.$i --mem=10G -o $prefix/mpileup/individual_bams/logs/$i.o -e $prefix/mpileup/individual_bams/logs/$i.e --time=500 -p akundaje,euan,owners,normal run_mpileup.sh $cur_bam $outf $ref
done
