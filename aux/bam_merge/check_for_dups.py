import pandas as pd 
import pdb 
data=pd.read_table("filtered_bams.txt",header=None,sep='/') 
counts=dict() 
for index,row in data.iterrows():
    biorep=row[10]
    biorep_hash=row[13] 
    print(biorep_hash) 
    if biorep not in counts: 
        counts[biorep]=dict() 
    if biorep_hash not in counts[biorep]: 
        counts[biorep][biorep_hash]=[row] 
    else: 
        counts[biorep][biorep_hash].append(row) 
outf=open("filtered_nodup_bams.txt",'w') 
for biorep in counts: 
    first_hash=list(counts[biorep].keys())[0] 
    lines=counts[biorep][first_hash]
    for line in lines: 
        outf.write('/'.join([str(i) for i in line])+'\n')


    
