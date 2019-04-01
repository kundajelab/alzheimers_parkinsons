import pandas as pd
import argparse
def parse_args():
    parser=argparse.ArgumentParser("truncated a narrowPeak file to specified interval around summit")
    parser.add_argument("--input_bed")
    parser.add_argument("--summit_flank",type=int,default=100)
    parser.add_argument("--outf")
    return parser.parse_args()

def main():
    args=parse_args()
    data=pd.read_csv(args.input_bed,header=None,sep='\t')
    print("loaded data!")
    chrom=data[0]
    startpos=data[1]
    summit_pos=startpos+data[9]
    adjusted_start=summit_pos-args.summit_flank
    adjusted_end=summit_pos+args.summit_flank
    print("got the adjusted coordinates")
    coord=pd.concat([chrom,adjusted_start,adjusted_end],axis=1)
    coord.to_csv(args.outf,sep='\t',header=False,index=False)
    
    
if __name__=="__main__":
    main()
    
