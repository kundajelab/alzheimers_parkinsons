import argparse
def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("--perf_metric_files",nargs="+")
    parser.add_argument("--outf")
    parser.add_argument("--cluster_pos_in_name",type=int,default=1)
    parser.add_argument("--name_delim",default='.')
    return parser.parse_args()

def main():
    args=parse_args()
    outf=open(args.outf,'w')
    outf.write('Cluster\tSplit\tMetric\tValue\n')
    for fname in args.perf_metric_files:
        prefix=fname.split('/')[-1].split(args.name_delim)[args.cluster_pos_in_name]
        data=open(fname,'r').read().strip().split('\n')
        for line in data[1::]:
            outf.write(prefix+'\t'+line+'\n')

if __name__=="__main__":
    main()
    
