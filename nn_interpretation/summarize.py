#generate plots for snps
import argparse
import pickle
from dragonn.vis import *
import os.path
import pandas as pd 
import numpy as np
import pdb

def parse_args():
    parser=argparse.ArgumentParser(description="assign SNP pvalues")
    parser.add_argument("--input_pickle")
    parser.add_argument("--cluster") 
    parser.add_argument("--fold")
    parser.add_argument("--regression_classification")
    parser.add_argument("--snp_flank",type=int,default=10,help="one sided flank" )
    parser.add_argument("--sig_snps")
    parser.add_argument("--out_prefix")
    return parser.parse_args()

def summarize_signal(sig,snp_flank):
    #get the absolute value
    sig=sig.squeeze()
    print(sig.shape) 
    abs_sig=np.absolute(sig)
    sig_shape=sig.shape[0]
    sig_center=int(sig.shape[1]/2)
    print(sig_center)
    abs_sig_total_sum=[abs_sig[i].sum() for i in range(sig_shape)]
    abs_sig_center_sum=[abs_sig[i,sig_center-snp_flank:sig_center+snp_flank,:].sum() for i in range(sig_shape)]
    #compute ratio of signal in SNP region over total signal
    snp_sig_ratio=[abs_sig_center_sum[i]/abs_sig_total_sum[i] for i in range(len(abs_sig_total_sum))]
    #is the maximum signal in thte track overlapping the SNP region?
    sig_max_pos=[np.argmax(np.max(abs_sig[i],axis=-1),axis=0) for i in range(abs_sig.shape[0])]
    sig_max_pos_near_snp=[(i<=sig_center+snp_flank)&(i>=sig_center-snp_flank) for i in sig_max_pos]
    return abs_sig_total_sum,abs_sig_center_sum,snp_sig_ratio,sig_max_pos,sig_max_pos_near_snp
    

def main():
    args=parse_args()
    #load the input pickle
    data=pickle.load(open(args.input_pickle,'rb'))
    print("loaded data") 
    snps=data['rsid']
    gradxinput_delta=data['gradxinput_delta']
    grad_abs_sig_total_sum,grad_abs_sig_center_sum,grad_snp_sig_ratio,grad_sig_max_pos,grad_sig_max_pos_near_snp=summarize_signal(gradxinput_delta,args.snp_flank)
    print("summarized gradxinput signal")
    ismxinput=data['ismxinput']
    ism_abs_sig_total_sum,ism_abs_sig_center_sum,ism_snp_sig_ratio,ism_sig_max_pos,ism_sig_max_pos_near_snp=summarize_signal(ismxinput,args.snp_flank)
    print("summarized ism signal") 
    outf=open(args.out_prefix+"summaries."+str(args.cluster)+"."+str(args.fold)+"."+str(args.regression_classification)+".txt",'w')
    outf.write('rsid\tSVMSig\tGradTotalSignal\tGradSNPSignal\tGradSignalRatio\tGradMaxPos\tGradMaxPosNearSNP\tISMTotalSignal\tISMSNPSignal\tISMSignalRatio\tISMMaxPos\tISMMaxPosNearSNP\n')
    sig_snps=pd.read_csv(args.sig_snps,header=0,sep='\t')
    sig_snp_dict=dict()
    for index,row in sig_snps.iterrows():
        sig_snp_dict[row['rsid']]=1 
    for i in range(len(snps)):
        cursnp=snps[i]
        if cursnp in sig_snp_dict:
            isSig=True
        else:
            isSig=False
        outf.write('\t'.join([str(j) for j in [snps[i],
                                               isSig,
                                               round(grad_abs_sig_total_sum[i],2),
                                               round(grad_abs_sig_center_sum[i],2),
                                               round(grad_snp_sig_ratio[i],2),
                                               round(grad_sig_max_pos[i],2),
                                               grad_sig_max_pos_near_snp[i],
                                               round(ism_abs_sig_total_sum[i],2),
                                               round(ism_abs_sig_center_sum[i],2),
                                               round(ism_snp_sig_ratio[i],2),
                                               round(ism_sig_max_pos[i],2),
                                               ism_sig_max_pos_near_snp[i]]])+'\n')

if __name__=="__main__":
    main()
    

