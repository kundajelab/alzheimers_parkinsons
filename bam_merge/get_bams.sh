source_dir=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/
find $source_dir -wholename "*call-filter*pe.q10.sort.rmdup.nodup.bam" | grep -v "inputs" | grep -v "glob" | grep -v "duplicate" > filtered_bams.txt 

