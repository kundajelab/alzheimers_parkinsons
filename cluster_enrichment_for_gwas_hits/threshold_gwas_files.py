#bin gwas snps by log10 scale, create bed files 
import argparse
import pandas as pd
import numpy as np 
import math
import pdb

def parse_args():
    parser=argparse.ArgumentParser(description="bin gws snps by log10 scale, create bed files")
    parser.add_argument("--gwas")
    parser.add_argument("--out_prefix")
    parser.add_argument("--append",action="store_true",default=False,help="prepends prefix 'chr' to chromosome name")
    return parser.parse_args()
def main():
    args=parse_args()
    gwas=pd.read_csv(args.gwas,header=0,delim_whitespace=True,dtype={'chr':'str'})
    if args.append is True: 
        gwas['chr']='chr'+gwas['chr']
    gwas['start_pos']=gwas['snp_pos']-1
    print("loaded gwas!")
    gwas['logp']=np.log10(gwas['pvalue'])
    for thresh in [-1,-2,-3,-4,-5,-6,-7,-8,-9,-10]:
        print(thresh) 
        subset=gwas[gwas['logp']<thresh][['chr','start_pos','snp_pos','rsid']]
        subset.to_csv(args.out_prefix+"."+str(thresh)+".bed",index=False,header=False,sep='\t')
    print("saving full gwas")
    subset=gwas[['chr','start_pos','snp_pos','rsid']]
    subset.to_csv(args.out_prefix+".bed",index=False,header=False,sep='\t')
if __name__=="__main__":
    main()
    
