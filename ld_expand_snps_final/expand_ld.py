import tabix
import pandas as pd
import pdb
import argparse

def parse_args():
    parser=argparse.ArgumentParser(description="LD expand all SNPs in a given file set")
    parser.add_argument("--snp_pos_bed_file")
    parser.add_argument("--LD_file",default="LD/EUR_geno.txt.gz")
    parser.add_argument("--outf")
    return parser.parse_args()

def main():
    args=parse_args()
    ld_data=tabix.open(args.LD_file)
    print("opened tabixed LD file for reading")
    snps=pd.read_csv(args.snp_pos_bed_file,header=0,sep='\t')
    print(snps.shape) 
    outf=open(args.outf,'w')
    outf.write('\t'.join(['LD_snp_chrom','LD_snp_0ind_pos','LD_snp_1ind_pos','LD_rs','LD_val'])+'\t'+'\t'.join(snps.columns)+'\n')
    for index,row in snps.iterrows():
        if index %100000==0:
            print(index)
        row_string='\t'.join([str(i) for i in row])
        try:
            #chrom_hg19      snp_pos_hg19_0  snp_pos_hg19
            ld_snps=ld_data.query(row['chrom_hg19'],row['snp_pos_hg19_0'],row['snp_pos_hg19'])
            #get the min and max position of the overlap
            ld_snps=[i for i in ld_snps]
            
            if len(ld_snps)==0:
                #nothing in ld found, just use the original snp entry
                ld_info='\t'.join([str(i) for i in [row['chrom_hg19'], row['snp_pos_hg19_0'], row['snp_pos_hg19'], row['snp_id'], 1]])
                outf.write(ld_info+'\t'+row_string+'\n')
            else:
                for entry in ld_snps:
                    #pdb.set_trace() 
                    ld_info='\t'.join([str(i) for i in entry[4::]])
                    outf.write(ld_info+'\t'+row_string+'\n')
        except:
            ld_info='\t'.join([str(i) for i in [row['chrom_hg19'], row['snp_pos_hg19_0'], row['snp_pos_hg19'], row['snp_id'], 1]])
            outf.write(ld_info+'\t'+row_string+'\n')
            
if __name__=="__main__":
    main()
    
