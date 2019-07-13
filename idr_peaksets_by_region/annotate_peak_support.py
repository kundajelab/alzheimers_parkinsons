import pdb
import argparse
import pandas as pd 
import pybedtools 

def parse_args(): 
    parser=argparse.ArgumentParser(description="annotate peaks assigned to regions with IDR pvalues and number of supporting samples")
    parser.add_argument("--peak_set") 
    parser.add_argument("--supporting_files", help="file with list of supporting files")
    parser.add_argument("--outf")
    parser.add_argument("--base_overlap_thresh",type=int,default=200,help="number of bases that must overlap between IDR peak and source sample peak")
    return parser.parse_args()

def main(): 
    args=parse_args() 
    peak_dict=dict() 
    print("indexed peak set") 
    pybed_merged=pybedtools.BedTool(args.peak_set)
    for row in pybed_merged: 
        peak_dict[(row[0],int(row[1]),int(row[2]))]=[[],set([])] 
    print("generated merged peak set") 
    supporting_files=open(args.supporting_files,'r').read().strip().split('\n') 
    n_contributing_files=len(supporting_files) 

    for f in supporting_files: 
        print(f)
        basename=f.split('/')[10]
        data=pd.read_table(f,header=None,sep='\t')
        try:
            pybed_data=pybedtools.BedTool(f)
        except: 
            print("Could not load:"+str(f)+"; skipping!")
            continue 
        #generate a bedtools intersection with the merged peak set and the contributing file. Use the wo flag so we can map 
        #back to which merged peaks intersect which source peaks. 
        try:
            intersections=pybed_merged.intersect(pybed_data,wo=True) 
        except: 
            print("Could not intersect:"+str(f)+"; skipping!")
            continue 
        for row in intersections: 
            overlap=int(row[-1]) 
            if overlap < args.base_overlap_thresh:
                continue 
            merged_peak=(row[0],int(row[1]),int(row[2]))
            pval=float(row[-4])
            assert merged_peak in peak_dict 
            peak_dict[merged_peak][0].append(pval) 
            peak_dict[merged_peak][1].add(basename) 

    print("finished parsing contributing files, summarizing peak summary stats") 
    outf=open(args.outf,'w') 
    outf.write('CHROM\tSTART\tEND\tMIN_PVAL\tMAX_PVAL\tN_SUPPORTING_SAMPLES\tN_CANDIDATE_SAMPLES\n')
    outf_expanded=open(args.outf+".expanded",'w')
    outf_expanded.write('CHROM\tSTART\tEND\tPVAL\tSUPPORTING_SAMPLES\n')
    for peak in peak_dict: 
        if len(peak_dict[peak][0])<1: 
            print("Skipping:"+str(peak))
            continue 
        out_string_expanded=[peak[0],str(peak[1]),str(peak[2]),','.join([str(i) for i in peak_dict[peak][0]]),','.join(list(peak_dict[peak][1]))]
        outf_expanded.write('\t'.join(out_string_expanded)+'\n')
        #get the summary statistics 
        min_pval=min(peak_dict[peak][0]) 
        max_pval=max(peak_dict[peak][0]) 
        num_supporting_samples=len(list(peak_dict[peak][1]))
        out_string=[peak[0],str(peak[1]),str(peak[2]),str(min_pval),str(max_pval),str(num_supporting_samples),str(n_contributing_files)]
        outf.write('\t'.join(out_string)+'\n')

if __name__=="__main__": 
    main() 
