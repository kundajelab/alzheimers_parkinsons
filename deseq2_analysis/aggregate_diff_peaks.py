#summarize the deseq2 analysis results across the different cohorts.
import argparse
from os import listdir
from os.path import isfile, join
import pandas as pd

def parse_args():
    parser=argparse.ArgumentParser(description="summarize differential peak counts for upregulated/downregulated peaks across the different AD/PD comparisons")
    parser.add_argument("--AD_dir",default="AD")
    parser.add_argumetn("--PD_dir",default="PD")
    parser.add_argument("--outf_region_type",default="deseq2_diff_peak_counts_region_type.tsv")
    parser.add_argument("--outf_regionmod_typemod",default="deseq2_diff_peak_counts_regionmod_typemod.tsv")
    return parser.parse_args()

def main():
    args=parse_args()
    outf=open(args.outf,'w')
    header=['Cohort','Region','Type1','Type2','P-val<0.5_nosva','Up Type1_nosva','Down Type1_nosva','P-val<0.5_sva','Up Type1_sva','Down Type1_sva']
    outf_region_type=open(args.outf_region_type,'w')
    outf_regionmod_typemod=open(args.outf_regionmod_typemod,'w')
    outf_region_type=open(args.outf_region_type,'w')
    ad_files=[f for f in listdir(args.AD_dir) if isfile(join(args.AD_dir,f))]
    pd_files=[f for f in listdir(args.PD_dir) if isfile(join(args.PD_dir,f))]
    for f in ad_files:
        if f.endswith('tsv'):
            #parse the file name 
            if f.startswith('sva'):
                if f.__contains__('expanded'):
                    #sva expanded
                    
if __name__=="__main__":
    main()
    
