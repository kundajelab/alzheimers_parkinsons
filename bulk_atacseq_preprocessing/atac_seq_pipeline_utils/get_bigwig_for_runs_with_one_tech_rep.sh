find /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/ -name "*.fc.signal.bigwig" | grep -v "/inputs/" | grep -v "glob" | grep -v "null" | grep -f to_rerun_fc.bigwig.txt &>> nodup.tn5.pooled.fc.signal.bigwig

find /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/ -name "*.pval.signal.bigwig" | grep -v "/inputs/" | grep -v "glob" | grep -v "null" | grep -f to_rerun_pval.bigwig.txt &>> nodup.tn5.pooled.pval.signal.bigwig

