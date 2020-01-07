echo "#!/bin/bash" > header
for f in `cut -f1 groups.txt`
do
    echo "field:"$f
    echo "samtools merge /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/merged_bams/$f.bam" > merge_bam_$f.sh 
    grep $f filtered_nodup_bams.txt | cut -f2 >> merge_bam_$f.sh
    cat merge_bam_$f.sh | tr '\n' ' ' > tmp 
    cat header tmp > merge_bam_$f.sh 
    rm tmp 
done
