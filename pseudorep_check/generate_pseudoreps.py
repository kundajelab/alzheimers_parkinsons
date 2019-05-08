import argparse 
import pandas as pd 
import gzip
import io
import random 

def parse_args(): 
    parser=argparse.ArgumentParser(description="") 
    parser.add_argument('-i',help="gzipped input tagAlign file") 
    parser.add_argument('-nreps',type=int,help="number of pseudoreplicates to generate")
    parser.add_argument('-outprefix',help='output prefix for the generated pseudoreplicates')
    parser.add_argument('-counter_print',type=int,default=100000,help="how many lines to parse before printing the current counter")
    return parser.parse_args() 
    
def main(): 
    args=parse_args() 
    gz = gzip.open(args.i, 'rb')
    f = io.BufferedReader(gz)
    outfiles=[gzip.open(args.outprefix+'.'+str(i),'wb') for i in range(args.nreps)]
    out_file_indices=list(range(args.nreps))
    counter=0
    for line in f:
        counter+=1 
        if counter%args.counter_print==0: 
            print(counter) 
        #randomly assign to replicates 
        cur_out_file=random.sample(out_file_indices,1)[0] 
        outfiles[cur_out_file].write(line)
    #close all the pseudorep output files 
    for i in range(len(outfiles)): 
        outfiles[i].close() 

    
if __name__=="__main__": 
    main() 

