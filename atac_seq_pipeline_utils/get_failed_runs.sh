#narrowPeaks
#python get_failed_runs.py --input_jsons /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/jsons --output_files /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/narrowPeak.files.nodup.txt --outf to_rerun_narrowPeak.txt

#tagAligns 
#python get_failed_runs.py --input_jsons /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/jsons --output_files /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/nodup.tn5.pooled.tagAlign.files.nodup.txt --outf to_rerun_tagAlign.txt

#fc bigWig 
#python get_failed_runs.py --input_jsons /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/jsons --output_files /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/nodup.tn5.pooled.fc.signal.nodup.bigwig --outf to_rerun_fc.bigwig.txt

#pval bigWig 
#python get_failed_runs.py --input_jsons /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/jsons --output_files /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/nodup.tn5.pooled.pval.signal.nodup.bigwig --outf to_rerun_pval.bigwig.txt

#ataqc jsons 
python get_failed_runs.py --input_jsons /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/jsons --output_files /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/ataqc.json --outf to_rerun_ataqc.txt
