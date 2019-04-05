import argparse 
def parse_args(): 
    parser=argparse.ArgumentParser() 
    parser.add_argument("--inputf",default="/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/optimal.idr.narrowPeaks.txt") 
    parser.add_argument("--outf",default="/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/tmp") 
    parser.add_argument("--num_splits",type=int,default=11) 
    return parser.parse_args() 
def main(): 
    args=parse_args() 
    outf=open(args.outf,'w') 
    data=open(args.inputf,'r').read().strip().split('\n') 
    section_dict=dict() 
    for line in data: 
        prefix='/'.join(line.split('/')[0:args.num_splits])
        section_dict[prefix]=line 
    for key in section_dict: 
        outf.write(section_dict[key]+'\n')
        
    
if __name__=="__main__": 
    main() 
