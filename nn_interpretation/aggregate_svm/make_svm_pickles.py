import argparse
import pandas as pd
import numpy as np
import pickle

def parse_args():
    parser=argparse.ArgumentParser(description="aggregate svm scores to pickle format for compatibility with NN scores")
    parser.add_argument("--score_dir",default="/mnt/lab_data3/soumyak/adpd/explain_scores")
    parser.add_argument("--snp_dir",default="/mnt/lab_data3/soumyak/adpd/snp_lists")
    return parser.parse_args()

def main():
    args=parse_args()
    for cluster in range(1,25):
        snps=list(pd.read_csv(args.snp_dir+'/'+"Cluster"+str(cluster)+".overlap.expanded.snps.hg38.bed",header=0,sep='\t')['rsid'])
        for fold in range(0,10):
            effect_numpy=[]
            noneffect_numpy=[]
            delta_numpy=[] 
            effect_scores=pd.read_csv(args.score_dir+'/'+"Cluster"+str(cluster)+"/"+"fold"+str(fold)+".effect.scores.txt",header=None,sep='\t')
            noneffect_scores=pd.read_csv(args.score_dir+'/'+"Cluster"+str(cluster)+"/"+"fold"+str(fold)+".noneffect.scores.txt",header=None,sep='\t')
            for index in range(len(snps)): 
                cur_effect=np.array([[float(j) for j in i.split(',')] for i in effect_scores.iloc[index][2].split(';')])
                cur_noneffect=np.array([[float(j) for j in i.split(',')] for i in noneffect_scores.iloc[index][2].split(';')])
                cur_delta=cur_effect - cur_noneffect
                effect_numpy.append(cur_effect)
                noneffect_numpy.append(cur_noneffect)
                delta_numpy.append(cur_delta)
            #save to pickle
            outputs={'rsid':snps,
                     'gkm_effect':effect_numpy,
                     'gkm_noneffect':noneffect_numpy,
                     'gkm_delta':delta_numpy}
            pickle.dump(outputs,open('gkm.Cluster'+str(cluster)+'.fold'+str(fold)+'.pl','wb'))

            
            

if __name__=="__main__":
    main()
    
