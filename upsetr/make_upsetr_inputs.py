import argparse
import pandas as pd 
def parse_args():
    parser=argparse.ArgumentParser(description="Generate input matrix for R UpsetR package to compare across limma differential peak sets ")
    parser.add_argument("--limma_diff_peaks",nargs="+")
    parser.add_argument("--outf")
    return parser.parse_args()

def main():
    args=parse_args()
    diff_dict=dict() # chrom_start_end --> sample --> 1
    samples=list(args.limma_diff_peaks)
    samples_stripped=[i.split('/')[-1].split('.')[0] for i in samples]
    outf=open(args.outf,'w')
    outf.write("Chrom_Start_End"+'\t'+'\t'.join(samples_stripped)+'\n')
    for sample in samples:
        print(sample)
        try:
            data=pd.read_csv(sample,header=0,sep='\t',index_col=0)
        except:
            continue 
        for index,row in data.iterrows():
            if index not in diff_dict:
                diff_dict[index]=dict()
            diff_dict[index][sample]=1
    print("writing outputs")
    for region in diff_dict:
        outf.write(region)
        for sample in samples:
            if sample in diff_dict[region]:
                outf.write('\t1')
            else:
                outf.write('\t0')
        outf.write('\n')
        
if __name__=="__main__":
    main()
    
