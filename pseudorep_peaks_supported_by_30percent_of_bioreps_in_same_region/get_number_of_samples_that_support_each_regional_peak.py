#using IDR optimal peaks from the pseudoreplicate set, calculate the number of biological replicates (based on biorep IDR optimal peak sets) that support each peak
import argparse 
import pybedtools 
import gzip
def parse_args(): 
    parser=argparse.ArgumentParser(description="using IDR optimal peaks from the pseudoreplicate set, calculate the number of biological replicates (based on biorep IDR optimal peak sets) that support each peak")
    parser.add_argument("--pseudorep_idr_optimal_peaks",help="file containing full paths to the pseudorep IDR peak sets") 
    parser.add_argument("--biorep_idr_optimal_peaks",help="file containing full paths to the biorep IDR peak sets")
    parser.add_argument("--samples",help="file containing list of samples to annotate")
    parser.add_argument("--thresh",default=0.3,type=float,help="percent of bioreps for a given condition/region that must contain a peak for it to be included in the finalized set")
    parser.add_argument("--out_suffix",default=".idr.optimal_peaks.support30%.bed.gz",help="file suffix for the sample output peak file prefix")
    return parser.parse_args() 

def get_sample_to_pseudorep_peak_map(samples,pseudorep_idr_optimal_peaks): 
    sample_to_pseudorep_peaks=dict() 
    for pseudorep_peakset in pseudorep_idr_optimal_peaks:
        for sample in samples: 
            if sample in pseudorep_peakset: 
                sample_to_pseudorep_peaks[sample]=pybedtools.bedtool.BedTool(pseudorep_peakset)
                break 
    return sample_to_pseudorep_peaks 

def get_sample_to_biorep_peak_map(samples,biorep_idr_optimal_peaks): 
    sample_to_biorep_peaks=dict() 
    for sample in samples: 
        sample_to_biorep_peaks[sample]=[] 
    for biorep_peakset in biorep_idr_optimal_peaks: 
        renamed=biorep_peakset.replace('/','_')
        for sample in samples: 
            if sample in renamed: 
                sample_to_biorep_peaks[sample].append(pybedtools.bedtool.BedTool(biorep_peakset) )
                break
    return sample_to_biorep_peaks


def main(): 
    args=parse_args() 
    pseudorep_idr_optimal_peaks=open(args.pseudorep_idr_optimal_peaks,'r').read().strip().split('\n') 
    biorep_idr_optimal_peaks=open(args.biorep_idr_optimal_peaks,'r').read().strip().split('\n')  
    samples=open(args.samples,'r').read().strip().split('\n') 
    sample_to_pseudorep_peaks=get_sample_to_pseudorep_peak_map(samples,pseudorep_idr_optimal_peaks)
    sample_to_biorep_peaks=get_sample_to_biorep_peak_map(samples,biorep_idr_optimal_peaks) 
    for sample in samples: 
        pseudorep_peaks=sample_to_pseudorep_peaks[sample] 
        support_histogram=dict() 
        for entry in pseudorep_peaks:
            support_histogram[tuple(entry[0:3])]=[0,entry] 
        for biorep_peaks in sample_to_biorep_peaks[sample]: 
            #intersect them 
            intersection=pseudorep_peaks.intersect(biorep_peaks,u=True,f=0.4,F=0.4,e=True)
            intersection=list(set([tuple(i[0:3]) for i in intersection]))
            print(str(len(intersection))+"/"+str(len(pseudorep_peaks)))
            for intersection_entry in intersection: 
                support_histogram[intersection_entry][0]+=1 
        outf=gzip.open(sample+args.out_suffix,'wt')
        outf_bad=gzip.open(sample+".unsupported"+args.out_suffix,'wt')
        min_support_count=args.thresh*len(sample_to_biorep_peaks[sample])
        print("min_support_count:"+str(min_support_count))
        out_good=[]
        out_bad=[]
        for entry in support_histogram:
            cur_entry_support=support_histogram[entry][0]
            if cur_entry_support >= min_support_count: 
                out_good.append(str(support_histogram[entry][1]).rstrip('\n')+'\t'+str(cur_entry_support))
            else: 
                out_bad.append(str(support_histogram[entry][1]).rstrip('\n')+'\t'+str(cur_entry_support))
        outf.write('\n'.join(out_good))
        outf_bad.write('\n'.join(out_bad))
        outf.close() 
        outf_bad.close() 

if __name__=="__main__": 
    main() 

