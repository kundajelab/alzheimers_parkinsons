import argparse 
import pdb

def parse_args(): 
    parser=argparse.ArgumentParser(description="tally number of samples that a peak appears in")
    parser.add_argument("--intersections",nargs="+") 
    parser.add_argument("--outf") 
    return parser.parse_args() 

def main(): 
    args=parse_args() 
    outf=open(args.outf,'w') 
    outf.write("Chrom\tStart\tEnd\tMaxPvalue\tMinPvalue\tMaxQvalue\tMinQvalue\tNumSamples\tSamples\n")


    #(chr,start,end)-->[files with this peak]
    peak_dict=dict() 
    for filename in args.intersections: 
        print(filename)
        data=open(filename,'r').read().strip().split('\n')  
        print(len(data))
        for line in data: 
            if line in peak_dict: 
                peak_dict[line].append(filename)
            else: 
                peak_dict[line]=[filename] 

    #write outputs 
    for peak in peak_dict: 
        num_hits=len(peak_dict[peak])
        outf.write(peak+'\t'+str(num_hits)+'\t'+','.join(peak_dict[peak])+'\n')

if __name__=="__main__": 
    main() 
