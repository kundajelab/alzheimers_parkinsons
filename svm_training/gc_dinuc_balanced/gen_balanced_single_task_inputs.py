#helper script for generating dinucleotide-balanced single task inputs from a single-input multi-output label file.
#assumes change_negs script has been executed to generated balanced negative sets for each task.
import argparse
import numpy as np
import pandas as pd
import pdb
def parse_args():
    parser=argparse.ArgumentParser(description="generate single task inputs from dinucleotide-matched positive and negative sets")
    parser.add_argument('--train_all_labels')
    parser.add_argument('--valid_all_labels')
    parser.add_argument('--test_all_labels')
    parser.add_argument('--task_subset_prefix')
    parser.add_argument('--task_subset_suffix')
    parser.add_argument('--out_prefix')
    return parser.parse_args()

def main():
    args=parse_args()
    train_all_labels=pd.DataFrame.from_csv(args.train_all_labels,header=0,sep='\t',index_col=[0,1,2])
    validate_all_labels=pd.DataFrame.from_csv(args.valid_all_labels,header=0,sep='\t',index_col=[0,1,2])
    test_all_labels=pd.DataFrame.from_csv(args.valid_all_labels,header=0,sep='\t',index_col=[0,1,2])
    num_tasks=train_all_labels.shape[1]
    for i in range(num_tasks):
        #get the negative examples
        to_keep_indices=[int(j) for j in np.load(args.task_subset_prefix+'.'+str(i)+'.'+args.task_subset_suffix)]
        train_subset=train_all_labels.iloc[to_keep_indices,i].sample(frac=1) # make sure to shuffle pos & negative
        valid_subset=validate_all_labels.iloc[:,i].sample(frac=1)
        test_subset=test_all_labels.iloc[:,i].sample(frac=1)
        #generate output files
        train_subset.to_csv(args.out_prefix+".train."+str(i)+".bed",sep='\t')
        valid_subset.to_csv(args.out_prefix+".validate."+str(i)+".bed",sep='\t')
        test_subset.to_csv(args.out_prefix+".test."+str(i)+".bed",sep='\t')
        print('done with '+str(i))
        

        
if __name__=="__main__":
    main()
    

