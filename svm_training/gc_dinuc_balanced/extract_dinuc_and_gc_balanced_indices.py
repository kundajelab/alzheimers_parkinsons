import argparse
import pdb
import pandas as pd
import numpy as np 

def parse_args():
    parser=argparse.ArgumentParser(description="extract dinuc and gc balanced indices")
    parser.add_argument("--bed_label_file")
    parser.add_argument("--numpy_index_file")
    parser.add_argument("--task_index",type=int,default=0)
    parser.add_argument("--outf")
    return parser.parse_args()
def main():
    args=parse_args()
    data=pd.DataFrame.from_csv(args.bed_label_file,header=None,sep='\t',index_col=[0,1,2])
    indices=np.load(args.numpy_index_file)
    filtered=data.iloc[indices,args.task_index]
    filtered.to_csv(args.outf,sep='\t',index=True,header=False)
    

if __name__=="__main__":
    main()
    
