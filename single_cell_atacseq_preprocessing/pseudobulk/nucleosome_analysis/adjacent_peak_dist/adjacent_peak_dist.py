import pandas as pd
import pdb
all_dists=[] 
for i in range(1,24):
    peaks=pd.read_csv("/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/idr_peaks/Cluster"+str(i)+".idr.optimal.narrowPeak.gz",header=None,sep='\t')
    peaks=peaks.sort_values(by=[0,1,9])
    summits=peaks[1]+peaks[9]
    peak_dists=summits.diff()
    peak_dists=list(peak_dists[peak_dists>0])#ignore dist across chrom boundaries
    all_dists=all_dists+peak_dists
    print(len(all_dists))

outf=open('all_peak_dists.tsv','w')
outf.write('\n'.join([str(i) for i in all_dists]))

