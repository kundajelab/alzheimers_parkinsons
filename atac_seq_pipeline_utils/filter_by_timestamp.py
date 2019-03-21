import argparse 
import os

def parse_args(): 
    parser=argparse.ArgumentParser(description="filter files with specified prefix by timestamp and keep the most recent one")
    parser.add_argument("--dir_steps",type=int,help="number of directory branches in the prefix,i.e. number of slashes to consider",default=11) 
    parser.add_argument("--file_list") 
    parser.add_argument("--outf") 
    return parser.parse_args() 

def main(): 
    args=parse_args() 
    outf=open(args.outf,'w') 
    #create a dictionary of prefix -> most recent file 
    timestamp_dict=dict() 
    #iterate through all the files 
    files=open(args.file_list,'r').read().strip().split('\n') 
    for fname in files: 
        #get the current prefix 
        cur_dir='/'.join(fname.split('/')[0:args.dir_steps])
        print(cur_dir) 
        #get the timestamp
        cur_timestamp=os.path.getmtime(fname) 
        if cur_dir not in timestamp_dict: 
            timestamp_dict[cur_dir]=dict() 
            timestamp_dict[cur_dir]['timestamp']=cur_timestamp 
            timestamp_dict[cur_dir]['fname']=fname 
        elif cur_timestamp > timestamp_dict[cur_dir]['timestamp']: 
            timestamp_dict[cur_dir]['timestamp']=cur_timestamp 
            timestamp_dict[cur_dir]['fname']=fname 
    for cur_dir in timestamp_dict: 
        fname=timestamp_dict[cur_dir]['fname'] 
        outf.write(fname+'\n') 


if __name__=="__main__": 
    main() 
