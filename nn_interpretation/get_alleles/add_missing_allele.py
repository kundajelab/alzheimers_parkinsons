import pandas as pd
data=pd.read_csv("no_alleles.csv",header=0,sep='\t')
hits=pd.read_csv('hits',header=None,sep='\t')
hit_dict=dict()
for index,row in hits.iterrows():
    chrom=row[0]
    pos=row[1]
    rsid=row[2]
    ref=row[3]
    alt=row[4]
    hit_dict[rsid]=[ref,alt]
    hit_dict[str(chrom)+'_'+str(pos)]=[ref,alt]
print(hit_dict) 
for index,row in data.iterrows():
    rsid=row['rsid']
    try:
        alleles=hit_dict[rsid]
        print(alleles)
        data['effect_allele'][index]=alleles[1]
        data['noneffect_allele'][index]=alleles[0]
        print(data.iloc[index])
    except:
        #print(rsid)
        continue
data.to_csv("augmented.tsv",sep='\t',header=True,index=False,na_rep="NA")
