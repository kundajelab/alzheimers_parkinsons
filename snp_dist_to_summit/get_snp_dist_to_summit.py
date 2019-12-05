import argparse
import pybedtools 
def parse_args():
    parser=argparse.ArgumentParser(description="get snp distance to summit")
    parser.add_argument("--peak_prefix",default="/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/idr_peaks/Cluster")
    parser.add_argument("--peak_suffix",default=".idr.optimal.narrowPeak")
    parser.add_argument("--snps",default="snps.bed")
    parser.add_argument("--nclusters",type=int,default=24)
    parser.add_argument("--outf",default="snp_summit_dist.idr.txt") 
    return parser.parse_args()
def main():
    args=parse_args()
    #snp-->cluster-->summit dist 
    dist_dict=dict()
    snps=pybedtools.BedTool(args.snps)
    print("loaded snps")
    for cluster in range(1,args.nclusters+1):
        cluster_peaks=pybedtools.BedTool(args.peak_prefix+str(cluster)+args.peak_suffix)
        print('got intersections for cluster' + str(cluster))
        #intersect
        intersection=snps.intersect(cluster_peaks,wao=True)
        for entry in intersection:
            #print(entry)
            cur_snp=entry[3]
            if cur_snp not in dist_dict:
                dist_dict[cur_snp]=dict() 
            match=entry[4]
            #print(match)
            if match==".":
                #no peak intersection
                dist_dict[cur_snp][cluster]="NA"
            else:
                #get the summit distance
                print(entry[5])
                print(entry[13])
                summit_pos=int(entry[5])+int(entry[13])
                snp_pos=int(entry[1])
                dist=snp_pos-summit_pos
                if cluster not in dist_dict[cur_snp]:
                    dist_dict[cur_snp][cluster]=dist
                elif abs(dist)<abs(dist_dict[cur_snp][cluster]):
                    dist_dict[cur_snp][cluster]=dist
    print(dist_dict)
    outf=open(args.outf,'w')
    clusters=list(range(1,args.nclusters+1))
    outf.write('snp\t'+'\t'.join(['Cluster'+str(i) for i in clusters])+'\n')
    for snp in dist_dict:
        outf.write(snp)
        for cluster in clusters:
            outf.write('\t'+str(dist_dict[snp][cluster]))
        outf.write('\n')
        

if __name__=='__main__':
    main()
    
