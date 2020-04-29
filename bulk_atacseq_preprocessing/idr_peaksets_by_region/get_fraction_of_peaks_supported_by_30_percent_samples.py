from os import listdir
from os.path import isfile, join
import pandas as pd
all_dir="/home/groups/akundaje/annashch/alzheimers_parkinsons/bulk_atacseq_preprocessing/idr_peaksets_by_region/all_annotated"
control_dir="/home/groups/akundaje/annashch/alzheimers_parkinsons/bulk_atacseq_preprocessing/idr_peaksets_by_region/controls_annotated"
all_files = [f for f in listdir(all_dir) if isfile(join(all_dir, f))]
control_files = [f for f in listdir(control_dir) if isfile(join(control_dir, f))]
outf=open("fraction_of_peaks_supported_by_30_or_more_samples.txt",'w') 
outf.write("Region\tN_PEAKS_SUPPORTED_BY_30_PERCENT_SAMPLES\tN_PEAKS\tFRACT_PEAKS_SUPPORTED_BY_30_PERCENT_SAMPLES\n") 
for f in all_files: 
    if f.endswith('.annotated.txt') : 
        data=pd.read_csv('/'.join([all_dir,f]),header=0,sep='\t') 
        data.fract_support=data.N_SUPPORTING_SAMPLES/data.N_CANDIDATE_SAMPLES 
        min30=data[data.fract_support>=.30]
        num_min30=min30.shape[0] 
        total_peaks=data.shape[0] 
        high_support_peak_fract=num_min30/total_peaks 
        outf.write(f+'\t'+str(num_min30)+'\t'+str(total_peaks)+'\t'+str(high_support_peak_fract)+'\n')
for f in control_files: 
    if f.endswith('.annotated.txt') : 
        data=pd.read_csv('/'.join([control_dir,f]),header=0,sep='\t') 
        data.fract_support=data.N_SUPPORTING_SAMPLES/data.N_CANDIDATE_SAMPLES 
        min30=data[data.fract_support>=.30]
        num_min30=min30.shape[0] 
        total_peaks=data.shape[0] 
        high_support_peak_fract=num_min30/total_peaks 
        outf.write(f+'\t'+str(num_min30)+'\t'+str(total_peaks)+'\t'+str(high_support_peak_fract)+'\n')
outf.close() 

