import tabix
import pandas as pd
import pdb
import argparse

def parse_args():
    parser=argparse.ArgumentParser(description="LD expand all SNPs in a given file set")
    parser.add_argument("--snp_file")
    parser.add_argument("--LD_file",default="/mnt/lab_data/kundaje/users/pgreens/LD/EUR_geno.txt.gz")
    parser.add_argument("--outf")
    return parser.parse_args()

def main():
    args=parse_args()
    ld_data=tabix.open(args.LD_file)
    print("opened tabixed LD file for reading")
    snps=pd.read_csv(args.snp_file, sep='\t')
    outf=open(args.outf,'w')
    outf.write('\t'.join(['LD_chr','LD_start','LD_end','LD_rsid','LD_val'])+'\t'+'\t'.join(snps.columns)+'\n')
    for index,row in snps.iterrows():
        if index %100000==0:
            print(index)
        row_string='\t'.join([str(i) for i in row])
        try:
            ld_snps=ld_data.query(row['chr'],row['start'],row['end'])
            #get the min and max position of the overlap
            ld_snps=[i for i in ld_snps]
            if len(ld_snps) > 0:
                ld_info='\t'.join([str(i) for i in [row['chr'], row['start'], row['end'], row['rsid'], 1]])
                outf.write(ld_info+'\t'+row_string+'\n')
                for entry in ld_snps:
                    ld_info='\t'.join([str(i) for i in entry[4:]])
                    outf.write(ld_info+'\t'+row_string+'\n')
        except:
            ld_info='\t'.join([str(i) for i in [row['chr'], row['start'], row['end'], row['rsid'], 1]])
            outf.write(ld_info+'\t'+row_string+'\n')

if __name__=="__main__":
    main()

