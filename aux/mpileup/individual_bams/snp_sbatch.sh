#!/bin/bash
module load biology
module load bcftools
mpileups=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/individual_bams/mpileup_output/mpileups.txt
numfiles=`cat $mpileups| wc -l`
outdir=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/individual_bams/bcf_snps
logdir=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/individual_bams/logs
for i in `seq 1 $numfiles`
do
    cur_mpileup=`head -n $i $mpileups | tail -n1`
    echo $cur_mpileup
    cur_basename=`basename $cur_mpileup`
    outf=$outdir/$cur_basename
    echo $outf
    sbatch -J bcf.call.$i -o $logdir/$i.o -e $logdir/$i.e -p akundaje,euan,owners,normal --mem=10G --time=300 run_snps.sh $cur_mpileup $outf
done
