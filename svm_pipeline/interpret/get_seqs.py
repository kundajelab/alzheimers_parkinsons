import argparse
import pysam
import pandas as pd

def parse_args():
    parser=argparse.ArgumentParser(description="get reference and alternate allele fasta sequences for variants to be interpreted with gkmexplain")
    parser.add_argument("--variant_bed")
    parser.add_argument("--fasta_ref",default="/mnt/data/male.hg19.fa")
    parser.add_argument("--out_prefix")
    parser.add_argument("--flank",type=int,default=500)
    return parser.parse_args()

def main():
    args=parse_args()
    variants=pd.read_csv(args.variant_bed,header=None,sep='\t')
    #print("read in variant file")
    ref=pysam.FastaFile(args.fasta_ref)
    outf_noneffect=open(args.out_prefix+'.noneffect.fa','w')
    outf_effect=open(args.out_prefix+'.effect.fa','w')
    for index,row in variants.iterrows():
        chrom=row[0]
        varpos=row[1]
        effect_allele=row[4]
        noneffect_allele=row[5]
        rsid=row[3]
        coord_start=varpos-args.flank
        coord_end=coord_start+2*args.flank
        seq=ref.fetch(chrom,coord_start,coord_end)
        assert(len(seq)==2*args.flank)
        left_flank=seq[0:args.flank]
        right_flank=seq[args.flank+1::]
        noneffect_allele_seq=left_flank+noneffect_allele+right_flank
        effect_allele_seq=left_flank+effect_allele+right_flank
        noneffect_header=">"+'_'.join([chrom,str(varpos),noneffect_allele,effect_allele,rsid,noneffect_allele])
        effect_header=">"+'_'.join([chrom,str(varpos),noneffect_allele,effect_allele,rsid,effect_allele])
        outf_noneffect.write('\n'.join([noneffect_header,noneffect_allele_seq])+'\n')
        outf_effect.write('\n'.join([effect_header,effect_allele_seq])+'\n')
    outf_noneffect.close()
    outf_effect.close()
    

if __name__=="__main__":
    main()
    
    
