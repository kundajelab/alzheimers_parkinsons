#!/bin/bash

cluster=$1

models=/mnt/lab_data3/soumyak/adpd/gkmsvm
orig_indir=/mnt/lab_data3/soumyak/adpd/explain_inputs
split_indir=/mnt/lab_data3/soumyak/adpd/explain_split_inputs
outdir=/mnt/lab_data3/soumyak/adpd/explain_scores
prefix=Cluster

for task in $cluster
do
    [[ -d $split_indir/$prefix$task ]] || mkdir $split_indir/$prefix$task
    cd $split_indir/$prefix$task
    cp $orig_indir/$prefix$task.* $split_indir/$prefix$task/
    split -d -l 100 -a 3 $prefix$task.effect.fasta $prefix$task.effect.fasta.split
    split -d -l 100 -a 3 $prefix$task.noneffect.fasta $prefix$task.noneffect.fasta.split
    rm $split_indir/$prefix$task/$prefix$task.effect.fasta
    rm $split_indir/$prefix$task/$prefix$task.noneffect.fasta
done

cd /users/soumyak/alzheimers_parkinsons/svm_snp_scoring

[[ -d $outdir/logs ]] || mkdir $outdir/logs

for task in $cluster
do
    [[ -d $outdir/$prefix$task ]] || mkdir $outdir/$prefix$task
    [[ -d $outdir/$prefix$task/split_scores ]] || mkdir $outdir/$prefix$task/split_scores
    for fold in {0..9}
    do
        for allele in effect noneffect
        do
            for split in `ls $split_indir/$prefix$task/$prefix$task.$allele.fasta.split*`
            do
                [[ -f $outdir/$prefix$task/split_scores/fold$fold.$allele.scores.split${split:(-3)} ]] || echo $outdir/$prefix$task/split_scores/fold$fold.$allele.scores.split${split:(-3)}
                [[ -f $outdir/$prefix$task/split_scores/fold$fold.$allele.scores.split${split:(-3)} ]] || bash run_gkmexplain.sh $models/$prefix$task/fold$fold/train/train.output.model.txt $split $outdir/$prefix$task/split_scores/fold$fold.$allele.scores.split${split:(-3)} &
            done
        done
        wait
    done
done
