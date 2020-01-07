import argparse 
import pdb

def parse_args(): 
    parser=argparse.ArgumentParser(description="tally number of samples that a peak appears in")
    parser.add_argument("--intersections",nargs="+") 
    parser.add_argument("--outf_prefix") 
    return parser.parse_args() 

def main(): 
    args=parse_args() 
    out_files=dict() 


    #(chr,start,end)-->[files with this peak]
    peak_dict=dict() 
    for filename in args.intersections: 
        print(filename)
        out_files[filename]=open(args.outf_prefix+filename.split('/')[-1],'w')
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
        if num_hits==1: 
            cur_filename=peak_dict[peak][0]
            out_files[cur_filename].write(peak+'\n')
        else: 
            print(str(peak_dict[peak])+":"+str(num_hits))
if __name__=="__main__": 
    main() 
