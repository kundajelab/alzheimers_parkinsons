import pandas as pd
import pdb 
metrics=['GradTotalSignal','GradSignalRatio','ISMTotalSignal','ISMSignalRatio']
#metric-->snp-->cluster
metric_dict=dict()
#snp-->cluster 
metric_dict_thresholded=dict()

thresholds=open('../sig_95percentile_cluster1.txt','r').read().strip().split('\n')
threshold_dict=dict()
for line in thresholds:
    tokens=line.split('\t')
    modeltype=tokens[0]
    metric=tokens[1]
    thresh=float(tokens[2])
    threshold_dict[modeltype+'.'+metric]=thresh
print(threshold_dict)

for cluster in range(1,25):
    for modeltype in ['classification','regression']:
        stats=pd.read_csv('../sig.summaries.'+str(cluster)+".0."+modeltype+".txt",header=0,sep='\t')
        for index,row in stats.iterrows():
            snp=row['rsid']
            if snp not in metric_dict_thresholded:
                metric_dict_thresholded[snp]=dict()
            if cluster not in metric_dict_thresholded[snp]:
                metric_dict_thresholded[snp][cluster]=0 
            for metric in metrics:
                cur_val=row[metric]
                cur_metric=modeltype+'.'+metric
                if cur_metric not in metric_dict:
                    metric_dict[cur_metric]=dict()
                if snp not in metric_dict[cur_metric]:
                    metric_dict[cur_metric][snp]=dict()
                metric_dict[cur_metric][snp][cluster]=cur_val
                if cur_val>=threshold_dict[cur_metric]:
                    metric_dict_thresholded[snp][cluster]+=1
#write outputs
for metric in metric_dict:
    outf=open("sig.snps."+metric+".txt",'w')
    outf.write('SNP\t'+'\t'.join([str(i) for i in range(1,25)])+'\n')
    for snp in metric_dict[metric]:
        outf.write(snp)
        for cluster in range(1,25):
            outf.write('\t'+str(round(metric_dict[metric][snp][cluster],2)))
        outf.write('\n')

outf=open('sig.snps.metric.tally.txt','w')
outf.write('SNP\t'+'\t'.join([str(i) for i in range(1,25)])+'\n')
for snp in metric_dict_thresholded:
    outf.write(snp)
    for cluster in range(1,25):
        outf.write('\t'+str(metric_dict_thresholded[snp][cluster]))
    outf.write('\n')
    
