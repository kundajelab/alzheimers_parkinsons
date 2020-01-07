import pandas as pd 
import pdb 
data=pd.read_table("1000GP_Phase3/1000GP_Phase3_chr17.legend.gz",header=0,sep=',')
targets=open("legend_hits_uniqued",'r').read().strip().split('\n') 
target_dict=dict() 
for line in targets: 
    target_dict[line]=1
outf=open('rows_to_pull','w') 
for index,row in data.iterrows(): 
    if row[0] in target_dict: 
        outf.write(str(index)+'\t'+str(row)+'\n')

