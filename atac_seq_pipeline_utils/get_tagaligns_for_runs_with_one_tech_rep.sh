find /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/ -name "*.tn5.tagAlign.gz" | grep -v "/inputs/" | grep -v "glob" | grep -f to_rerun_tagAlign.txt &>> nodup.tn5.pooled.tagAlign.files.nodup.txt


