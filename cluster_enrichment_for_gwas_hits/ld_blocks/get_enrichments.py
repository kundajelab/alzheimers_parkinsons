import argparse
from pybedtools import BedTool
import pdb

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("--peak_bed",nargs="+")
    parser.add_argument("--gwas_thresh_bed",nargs="+")
    parser.add_argument("--gwas_all_bed")
    parser.add_argument("--outf")
    return parser.parse_args()

def main():
    args=parse_args()
    outf=open(args.outf,'w')

    #get the expected overlap
    cluster_expected=dict()
    gwas_all_bed=BedTool(args.gwas_all_bed)
    for cur_cluster in args.peak_bed:
        print(cur_cluster)
        cur_cluster_bed=BedTool(cur_cluster)
        cur_intersection=gwas_all_bed.intersect(cur_cluster_bed)
        cluster_expected[cur_cluster]=len(cur_intersection)/len(gwas_all_bed)
    print("got expected")
    
    vcf_to_size=dict()
    cluster_overlap=dict()
    for cur_gwas in args.gwas_thresh_bed:
        cur_gwas_bed=BedTool(cur_gwas)
        num_snps=len(cur_gwas_bed)
        vcf_to_size[cur_gwas]=num_snps
        cluster_overlap[cur_gwas]=dict() 
        for cur_cluster in args.peak_bed:
            cur_cluster_bed=BedTool(cur_cluster)
            intersections=cur_gwas_bed.intersect(cur_cluster_bed,u=True)
            cluster_overlap[cur_gwas][cur_cluster]=len(intersections)
    outf.write('Vcfbin\tCluster\tExpected\tObserved\tFold\n')
    
    for vcf in cluster_overlap: 
        for cluster in cluster_overlap[vcf]:
            cur_bin=vcf
            cur_cluster=cluster
            expected=cluster_expected[cluster]
            observed=cluster_overlap[vcf][cluster]/vcf_to_size[vcf]
            fold=observed/expected
            outf.write('\t'.join([str(i) for i in [cur_bin,cur_cluster,expected,observed,fold]])+'\n')
        
if __name__=="__main__":
    main() 
