from kerasAC.splits import *
import argparse
import pandas as pd

chrom_to_split=dict()
splits=[] 
for split in hg19_splits:
    splits.append(split) 
    test_chroms=hg19_splits[split]['test']
    for chrom in test_chroms:
        chrom_to_split[chrom]=split

def parse_args():
    parser=argparse.ArgumentParser("split SNP bed file by Deep Learning CV split")
    parser.add_argument("--bed")
    parser.add_argument("--chrom_field") 
    return parser.parse_args()

def main():
    args=parse_args()
    data=pd.read_csv(args.bed,header=0,sep='\t')
    print(data)
    out_files={}
    for split in splits:
        out_files[split]=open(args.bed+'.'+str(split),'w')
        out_files[split].write('\t'.join(data.columns)+'\n')
    for index,row in data.iterrows():
        chrom=str(row[args.chrom_field])
        if 'chr' not in chrom:
            chrom = 'chr' + chrom
        cur_split=chrom_to_split[chrom]
        out_files[cur_split].write('\t'.join([str(i) for i in row])+'\n')
        
if __name__=="__main__":
    main()
    
