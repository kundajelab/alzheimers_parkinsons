#summarize haplotype information 
import pandas as pd 
import pdb

mapt_hap_spec_snps=pd.read_csv("../../MAPT_HapSpecificSNPs.txt",header=0,sep='\t') 
hap_spec_snp_dict=dict() 
for index,row in mapt_hap_spec_snps.iterrows(): 
    hap_spec_snp_dict[row['name']]=1 
    

tokeep=pd.read_csv('../../chr17-only_dbsnp151_common_MAPT_HaplotypeRegion.txt',header=0,delim_whitespace=True) 
tokeep_dict=dict() 
for index,row in tokeep.iterrows(): 
    snp_name=row[2] 
    tokeep_dict[snp_name]='\t'.join([str(i) for i in row])

print("made dict of SNPs of interest") 
bim=pd.read_csv("chr17_phase3_bed_range.bim.names_resolved",header=None,delim_whitespace=True) 
bim_dict=dict() 
for index,row in bim.iterrows(): 
    snp=row[1] 
    a1=row[4]
    a2=row[5] 
    bim_dict[snp]=dict() 
    bim_dict[snp][1]=a1
    bim_dict[snp][2]=a2
print('made bim dict') 
blocks=pd.read_csv("plink.blocks.det.names_resolved",header=0,delim_whitespace=True) 
freqs=pd.read_csv("numeric_geno/plink.frq.hap",header=0,delim_whitespace=True) 
outf=open('chr17_dbSNP151_common_MAPT_HaplotypeRegion_PHASED.txt','w')

hp_to_snp=dict() 
for index,row in blocks.iterrows(): 
    cur_haploblock="H"+str(index+1)
    snps=row['SNPS'].split('|') 
    hp_to_snp[cur_haploblock]=snps
print("created haploblock->snp mapping")
hps=[]
snp_to_hp=dict() 
for index,row in freqs.iterrows(): 
    cur_hap=row['LOCUS'] 
    cur_freq=row['F']
    hap_name='_'.join([cur_hap,str(cur_freq)])
    hps.append(hap_name) 
    cur_string=row['HAPLOTYPE'] 
    for i in range(len(cur_string)): 
        try:
            cur_allele_numeric=cur_string[i] 
            cur_rs=hp_to_snp[cur_hap][i]
            cur_allele_letter=bim_dict[cur_rs][int(cur_allele_numeric)]
        except:
            pdb.set_trace() 
        if cur_rs not in snp_to_hp: 
            snp_to_hp[cur_rs]=dict() 
        snp_to_hp[cur_rs][hap_name]=cur_allele_letter 

outf.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO"+'\t'+'HapSpecificPrediction\t'+'\t'.join(hps)+'\n')
for snp in tokeep_dict: 
    if snp not in snp_to_hp: 
        continue
    outf.write(tokeep_dict[snp]) 
    if snp in hap_spec_snp_dict: 
        outf.write('\t1') 
    else: 
        outf.write('\t0') 
    for hp in hps: 
        if hp not in snp_to_hp[snp]: 
            outf.write('\t') 
        else: 
            outf.write('\t'+snp_to_hp[snp][hp]) 
    outf.write('\n') 

    

