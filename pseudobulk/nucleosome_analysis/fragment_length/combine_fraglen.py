import pandas as pd
import pdb 
master_dict=dict() 
for i in range(1,25):
    cur_clust=pd.read_csv("Cluster"+str(i)+".fraglen.gz",header=0,sep='\t',index_col=0)
    for index,row in cur_clust.iterrows():
        if index not in master_dict:
            master_dict[index]=row[0]
        else:
            master_dict[index]+=row[0]
outf=open('fragment_length_aggregated_across_clusters.txt','w')
for key in master_dict:
    outf.write(str(key)+'\t'+str(master_dict[key])+'\n')
    


