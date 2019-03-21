#identify pipeline runs that are missing a particular output file type 
import argparse 
def parse_args(): 
    parser=argparse.ArgumentParser(description="identify pipeline runs that are missing a particular output file type")
    parser.add_argument("--input_jsons",default="/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/jsons" )
    parser.add_argument("--output_files") 
    parser.add_argument("--output_file_token",type=int,default=10)
    parser.add_argument("--input_file_token",type=int,default=3)
    parser.add_argument("--outf") 
    return parser.parse_args()  
def main(): 
    args=parse_args() 
    processed_samples=set() 
    samples=set() 
    for entry in open(args.output_files,'r').read().strip().split('\n'): 
        tokens=entry.split('/')
        processed_sample=tokens[args.output_file_token]
        print(processed_sample) 
        processed_samples.add(processed_sample)
    for entry in open(args.input_jsons,'r').read().strip().split('\n'): 
        sample=entry.split('/')[args.input_file_token].split('.')[0] 
        samples.add(sample) 
        print(sample) 
    failed=samples-processed_samples 
    outf=open(args.outf,'w') 
    for f in failed: 
        outf.write(f+'\n')

if __name__=="__main__": 
    main() 
