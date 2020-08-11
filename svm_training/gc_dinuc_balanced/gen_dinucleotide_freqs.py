import argparse
from change_negs import *
import pysam
import pandas as pd
import pdb

def parse_args():
    parser=argparse.ArgumentParser(description="generate dinucleotide frequencies for a bed file")
    parser.add_argument("--bed_path", "-b")
    parser.add_argument("--ratio_neg_to_pos",nargs="+",type=float)
    parser.add_argument("--outf", "-o")
    parser.add_argument("--ref_fasta")
    parser.add_argument("--dinuc_freqs",default=None)
    parser.add_argument("--task",type=int,default=None)
    parser.add_argument("--gc",action="store_true")
    return parser.parse_args()

def get_balanced_negative(args):
    data=pd.read_csv(args.bed_path,header=None,sep='\t',index_col=[0,1,2])
    freqs=np.loadtxt(args.dinuc_freqs)#,skiprows=1)
    good_indices = np.where(freqs > 0.0)[0]
    freqs = freqs[good_indices]
    data = data.iloc[good_indices]
    print("bed file:"+str(data.shape))
    print("frequencies:"+str(freqs.shape))
    if args.task!=None:
        if args.gc==True:
            sampled_indices=negs_gcmatched_samp(data.iloc[:,args.task],freqs,args.ratio_neg_to_pos[args.task],args.outf+'.'+str(args.task))
        else:

            sampled_indices=negs_dinucmatched_samp(data.iloc[:,args.task],freqs,args.ratio_neg_to_pos[args.task],args.outf+'.'+str(args.task))
        filtered=data.iloc[sampled_indices,args.task]
        filtered.to_csv(args.outf,sep='\t',index=True,header=False)
    else:
        numtasks=data.shape[1]
        for task in range(numtasks):
            if args.gc==True:
                sampled_indices=negs_gcmatched_samp(data.iloc[:,task],freqs,args.ratio_neg_to_pos[task],args.outf+'.'+str(task))
            else:
                sampled_indices=negs_dinucmatched_samp(data.iloc[:,task],freqs,args.ratio_neg_to_pos[task],args.outf+'.'+str(task))
            print("generated negatives for task:"+str(task))
            filtered=data.iloc[sampled_indices,task]
            filtered.to_csv(args.outf+'.'+str(task),sep='\t',index=True,header=False)

def get_gc_mat(args):
    #open the reference file
    ref=pysam.FastaFile(args.ref_fasta)
    #load the train data as a pandas dataframe, skip the header
    data=pd.read_csv(args.bed_path,header=None,sep='\t',index_col=[0,1,2])
    bed_entries=[i for i in data.index]
    print("got the bed entries")
    cur_entry=0
    outf=open(args.outf,'w')
    for ind,entry in enumerate(bed_entries):
        #print(ind)
        seq=ref.fetch(entry[0],entry[1],entry[2]).upper()
        if 'N' in seq:
            gc_fract = -5.0
        else:
            gc_fract=(seq.count('G')+seq.count('C'))/float(len(seq))
        outf.write(str(gc_fract)+'\n')


def get_dinuc_mat(args):
    #open the reference file
    ref=pysam.FastaFile(args.ref_fasta)
    #load the train data as a pandas dataframe, skip the header
    data=pd.read_csv(args.bed_path,header=None,sep='\t',index_col=[0,1,2])
    bed_entries=[i for i in data.index]
    print("got the bed entries")
    freq_dict=dict()
    all_dinucs=['AA','AC','AG','AT','CA','CC','CG','CT','GA','GC','GG','GT','TA','TC','TG','TT']
    for dinuc in all_dinucs:
        freq_dict[dinuc]=dict()
    cur_entry=0
    for entry in bed_entries:
        seq=ref.fetch(entry[0],entry[1],entry[2]).upper()
        for k in freq_dict.keys():
            freq_dict[k][cur_entry]=0.0
        #get the dinucleotide frequencies
        for ind in range(999):
            try:
                freq_dict[seq[ind:ind+2]][cur_entry]+=1
            except:
                print(seq[ind:ind+2])
        cur_entry+=1
        if (cur_entry % 1000==0):
            print(str(cur_entry))
    print("got dinuc counts")
    outf=open(args.outf,'w')
    outf.write('\t'.join(all_dinucs)+'\n')
    for i in range(cur_entry):
        fract=[str(freq_dict[d][i]/1000) for d in all_dinucs]
        outf.write('\t'.join(fract)+'\n')

def main():

    args=parse_args()
    if args.dinuc_freqs==None:
        #generate and save the dinucleotide frequency matrix
        if args.gc==True:
            get_gc_mat(args)
        else:
            get_dinuc_mat(args)
    else:
        get_balanced_negative(args)


if __name__=="__main__":
    main()

