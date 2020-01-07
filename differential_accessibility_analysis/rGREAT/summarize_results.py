import pandas as pd
import argparse
def parse_args():
    parser=argparse.ArgumentParser(description="aggregate GO terms by frequency")
    parser.add_argument("--inputf",nargs="+")
    parser.add_argument("--outf")
    parser.add_argument('--hyper_adjp_bh_thresh',type=float,default=0.001)
    return parser.parse_args()

def main():
    args=parse_args()
    term_to_name=dict()
    term_to_samples=dict()
    for fname in args.inputf:
        print(fname)
        try:
            data=pd.read_table(fname,header=0,sep=',')
        except:
            continue 
        for index,row in data.iterrows():
            if row['Hyper_Adjp_BH']>args.hyper_adjp_bh_thresh:
                continue
            cur_id=row['ID']
            cur_name=row['name']
            if cur_id not in term_to_name:
                term_to_name[cur_id]=cur_name
            if cur_id not in term_to_samples:
                term_to_samples[cur_id]=[fname]
            else:
                term_to_samples[cur_id].append(fname)
    outf=open(args.outf,'w')
    outf.write("ID\tName\tNumSamplesWithSignificantHit\tSamplesWithSignificantHit\n")
    for term in term_to_name:
        outf.write(term+'\t'+term_to_name[term]+'\t'+str(len(term_to_samples[term]))+'\t'+','.join(term_to_samples[term])+'\n')
                
if __name__=="__main__":
    main()
    
