tss_vals=open('tss_enrichments.txt','r').read().strip().split('\n')
tss_dict=dict()
for line in tss_vals[1::]:
    tokens=line.split('\t')
    cluster=tokens[0]
    enrichment=tokens[1]
    tss_dict[cluster]=enrichment
    
perf=open('cluster.perf.txt','r').read().strip().split('\n')
metrics=set([])
metric_dict=dict()
for line in perf[1::]:
    tokens=line.split('\t')
    cluster=tokens[0]
    metric=tokens[2]
    metrics.add(metric) 
    value=tokens[3]
    if cluster not in metric_dict:
        metric_dict[cluster]={}
    if metric not in metric_dict[cluster]:
        metric_dict[cluster][metric]=[] 
    metric_dict[cluster][metric].append(float(value))

for cluster in metric_dict:
    for metric in metric_dict[cluster]:
        metric_dict[cluster][metric]=sum(metric_dict[cluster][metric])/len(metric_dict[cluster][metric])
print(metric_dict) 
metrics=list(metrics)
outf=open('cluster.perf.means.vs.tss.txt','w')
outf.write('Cluster\tTSSenrichment\t'+'\t'.join(metrics)+'\n')
for cluster in metric_dict:
    outf.write(cluster)
    outf.write('\t'+tss_dict[cluster])
    for metric in metrics:
        outf.write('\t'+str(round(metric_dict[cluster][metric],2)))
    outf.write('\n')
