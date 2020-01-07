#summarize the deseq2 analysis results across the different cohorts.
import argparse
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np 
import pdb 
def parse_args():
    parser=argparse.ArgumentParser(description="summarize differential peak counts for upregulated/downregulated peaks across the different AD/PD comparisons")
    parser.add_argument("--AD_dir",default="AD")
    parser.add_argument("--PD_dir",default="PD")
    parser.add_argument("--outf_region_type",default="deseq2_diff_peak_counts_region_type.tsv")
    parser.add_argument("--outf_regionmod_typemod",default="deseq2_diff_peak_counts_regionmod_typemod.tsv")
    return parser.parse_args()

def parse_file(fdir,f):
    fname=f.split('_')
    diff_index=fname.index('diff')
    cohort=fname[diff_index+1]
    region=fname[diff_index+2]
    type1=fname[diff_index+3]
    type2=fname[-1].split('.')[0]

    data=pd.read_table('/'.join([fdir,f]),header=0,sep='\t')
    num_up=np.sum(data['log2FoldChange']>0)
    num_down=np.sum(data['log2FoldChange']<0)
    num_dif=data.shape[0]
    out_line=[cohort,region,type1,type2,num_dif,num_up,num_down]
    return out_line

def main():
    args=parse_args()

    outf_region_type=open(args.outf_region_type,'w')
    outf_regionmod_typemod=open(args.outf_regionmod_typemod,'w')

    header=['Cohort','Region','Type1','Type2','P-val<0.5_nosva','Up Type1_nosva','Down Type1_nosva','P-val<0.5_sva','Up Type1_sva','Down Type1_sva']

    outf_region_type.write('\t'.join(header)+'\n')
    outf_regionmod_typemod.write('\t'.join(header)+'\n')
    
    ad_files=[f for f in listdir(args.AD_dir) if isfile(join(args.AD_dir,f))]
    pd_files=[f for f in listdir(args.PD_dir) if isfile(join(args.PD_dir,f))]
    out_dict=dict()
    for f in ad_files:
        if f.endswith('tsv'):
            #parse the file name
            out_line=parse_file(args.AD_dir,f)
            print(out_line)
            cur_key=tuple(out_line[0:4])
            if cur_key not in out_dict:
                out_dict[cur_key]=dict()
            for subkey in ['expanded','collapsed']:
                if subkey not in out_dict[cur_key]:
                    out_dict[cur_key][subkey]=dict()
                for lowestkey in ['sva','nosva']: 
                    if lowestkey not in out_dict[cur_key][subkey]:
                        out_dict[cur_key][subkey][lowestkey]=dict()
            if f.startswith('sva'):
                if f.__contains__('expanded'):
                    #sva expanded
                    out_dict[cur_key]['expanded']['sva']=out_line
                else:
                    #sva collapsed
                    out_dict[cur_key]['collapsed']['sva']=out_line
            else:
                if f.__contains__('expanded'):
                    #non-sva expanded
                    out_dict[cur_key]['expanded']['nosva']=out_line
                else:
                    #non-sva collapsed
                    out_dict[cur_key]['collapsed']['nosva']=out_line
                    
    for f in pd_files:
        if f.endswith('tsv'):
            #parse the file name
            out_line=parse_file(args.PD_dir,f)
            print(out_line)
            cur_key=tuple(out_line[0:4])
            if cur_key not in out_dict:
                out_dict[cur_key]=dict()
            for subkey in ['expanded','collapsed']:
                if subkey not in out_dict[cur_key]:
                    out_dict[cur_key][subkey]=dict()
                for lowestkey in ['sva','nosva']: 
                    if lowestkey not in out_dict[cur_key][subkey]:
                        out_dict[cur_key][subkey][lowestkey]=dict()
            if f.startswith('sva'):
                if f.__contains__('expanded'):
                    #sva expanded
                    out_dict[cur_key]['expanded']['sva']=out_line
                else:
                    #sva collapsed
                    out_dict[cur_key]['collapsed']['sva']=out_line
            else:
                if f.__contains__('expanded'):
                    #non-sva expanded
                    out_dict[cur_key]['expanded']['nosva']=out_line
                else:
                    #non-sva collapsed
                    out_dict[cur_key]['collapsed']['nosva']=out_line
                
    #write the expanded & collapsed output files
    
    for cur_key in out_dict:
        if 'expanded' in out_dict[cur_key]:
            if 'nosva' in out_dict[cur_key]['expanded']: 
                outf_region_type.write('\t'.join([str(i) for i in out_dict[cur_key]['expanded']['nosva']])+'\t')
            else:
                outf_region_type.write('\t'.join(['']*7)+'\t')
            if 'sva' in out_dict[cur_key]['expanded']:
                outf_region_type.write('\t'.join([str(i) for i in out_dict[cur_key]['expanded']['sva']])+'\n')
            else:
                outf_region_type.write('\t'.join(['']*7)+'\n')
        if 'collapsed' in out_dict[cur_key]:
            if 'nosva' in out_dict[cur_key]['collapsed']: 
                outf_regionmod_typemod.write('\t'.join([str(i) for i in out_dict[cur_key]['collapsed']['nosva']])+'\t')
            else:
                outf_regionmod_typemod.write('\t'.join(['']*7)+'\t')
            if 'sva' in out_dict[cur_key]['collapsed']:
                outf_regionmod_typemod.write('\t'.join([str(i) for i in out_dict[cur_key]['collapsed']['sva']])+'\n')
            else:
                outf_regionmod_typemod.write('\t'.join(['']*7)+'\n')
                
if __name__=="__main__":
    main()
    
