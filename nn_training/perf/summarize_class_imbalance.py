import pandas as pd 
data=pd.read_table('cluster.perf.txt',header=0,sep='\t')
outf=open('class.imbalance.txt','w')
outf.write('Cluster\tSplit\tNegPosRatio\tPos\tNeg\n')
val_dict=dict() 
for index,row in data.iterrows():
    cluster=row['Cluster']
    split=row['Split']
    if cluster not in val_dict:
        val_dict[cluster]=dict()
    if split not in val_dict[cluster]:
        val_dict[cluster][split]=dict() 
    if row['Metric']=="num_positives":
        val_dict[cluster][split]['pos']=row['Value']
    if row['Metric']=="num_negatives":
        val_dict[cluster][split]['neg']=row['Value']
print(val_dict)

for cluster in val_dict:
    for split in val_dict[cluster]:
        try:
            pos=val_dict[cluster][split]['pos']
            neg=val_dict[cluster][split]['neg']
            ratio=neg/pos
            outf.write('\t'.join([str(i) for i in [cluster,split,ratio,pos,neg]])+'\n')
        except:
            continue
