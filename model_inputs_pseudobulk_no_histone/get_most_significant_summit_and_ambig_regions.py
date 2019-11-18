import argparse
import pandas as pd

def parse_args():
    parser=argparse.ArgumentParser(description="identify most significant summit in pseudobulk region")
    parser.add_argument("--narrowPeak")
    parser.add_argument("--outf")
    return parser.parse_args() 
    
def main():
    args=parse_args()
    data=pd.read_csv(args.narrowPeak,header=None,sep='\t')
    region_dict=dict()
    for index, row in data.iterrows():
        region=(row[0],row[1],row[2])
        signal=row[6]
        if region not in region_dict:
            region_dict[region]={}
        region_dict[region][signal]=row 
    #filter to strongest region
    outf=open(args.outf,'w')
    for region in region_dict:
        #find max signal summit
        max_signal_summit=max(region_dict[region].keys())
        #get the corresponding row
        max_row=region_dict[region][max_signal_summit]
        outf.write('\t'.join([str(i) for i in max_row])+'\n')
        
        
    
if __name__=="__main__":
    main()
    
