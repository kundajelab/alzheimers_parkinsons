import pdb 
import pandas as pd
#this script adds a column (column 2) that is the 0-indexed position from Mike's ld buddies dataframe

data=pd.read_csv("snps_final/ld_buddies_table_stage2.tsv",header=0,sep='\t')
#remove snps that are not in hg19
data=data[data['chrom_hg19'].isna()==False]
#get 0 index
data['snp_pos_hg19_0']=data['snp_pos_hg19'].subtract(1)
names=list(data.columns)
names.remove('chrom_hg19')
names.remove('snp_pos_hg19')
names.remove('snp_pos_hg19_0') 
names=[ 'chrom_hg19', 'snp_pos_hg19_0','snp_pos_hg19']+names
data=data[names]



data['chrom_hg19']=['chr'+str(int(i)) for i in data['chrom_hg19']]
data['snp_pos_hg19_0']=data['snp_pos_hg19_0'].astype('int64')
data['snp_pos_hg19']=data['snp_pos_hg19'].astype('int64')

data.to_csv("snps.hg19.bed",index=False,sep='\t')
