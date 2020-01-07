import argparse
import pandas as pd
import numpy as np
import pickle

def parse_args():
    parser=argparse.ArgumentParser(description="aggregate svm scores to pickle format for compatibility with NN scores")
    parser.add_argument("--effect_file",default="nn.effect.scores.txt")
    parser.add_argument("--noneffect_file",default="nn.noneffect.scores.txt")
    parser.add_argument("--snp_file",default="nn_only_snps.bed")    
    return parser.parse_args()

def main():
    args=parse_args()
    #gkm.Cluster20.fold6.pl
    #cluster -> fold -> numpy 
    cluster_fold_dict=dict()
    snps=pd.read_csv(args.snp_file,header=0,sep='\t')
    effect=pd.read_csv(args.effect_file,header=None,sep='\t')
    noneffect=pd.read_csv(args.noneffect_file,header=None,sep='\t')
    for index,row in snps.iterrows():
        rsid=snps.iloc[index]['rsid']
        cluster=snps.iloc[index]['cluster']
        fold=snps.iloc[index]['fold']
        if cluster not in cluster_fold_dict:
            cluster_fold_dict[cluster]=dict()
        if fold not in cluster_fold_dict[cluster]:
            cluster_fold_dict[cluster][fold]=dict()
            cluster_fold_dict[cluster][fold]['rsid']=[]
            cluster_fold_dict[cluster][fold]['gkm_effect']=[]
            cluster_fold_dict[cluster][fold]['gkm_noneffect']=[]
            cluster_fold_dict[cluster][fold]['gkm_delta']=[]
            
        cur_effect=np.array([[float(j) for j in i.split(',')] for i in effect.iloc[index][2].split(';')])
        cur_noneffect=np.array([[float(j) for j in i.split(',')] for i in noneffect.iloc[index][2].split(';')])
        cur_delta=cur_effect-cur_noneffect
        cluster_fold_dict[cluster][fold]['rsid'].append(rsid)
        cluster_fold_dict[cluster][fold]['gkm_effect'].append(cur_effect)
        cluster_fold_dict[cluster][fold]['gkm_noneffect'].append(cur_noneffect)
        cluster_fold_dict[cluster][fold]['gkm_delta'].append(cur_delta)

    #aggregate summaries
    for cluster in cluster_fold_dict:
        for fold in cluster_fold_dict[cluster]:
            #save to pickle
            outputs=cluster_fold_dict[cluster][fold]
            pickle.dump(outputs,open('gkm.Cluster'+str(cluster)+'.fold'+str(fold)+'.pl','wb'))

            
            

if __name__=="__main__":
    main()
    
