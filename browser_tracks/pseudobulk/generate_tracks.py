import json 
import argparse 
def parse_args(): 
    parser=argparse.ArgumentParser(description="generate pval & fc bigwig tracks")
    parser.add_argument("--pval_bigwigs")
    parser.add_argument("--fc_bigwigs") 
    parser.add_argument("--hammocks")
    parser.add_argument("--rna_bigwigs")
    parser.add_argument("--bams") 
    parser.add_argument("--sample_index",type=int)
    parser.add_argument("--outf_fc_bigwig") 
    parser.add_argument("--outf_pval_bigwig")
    parser.add_argument("--mitra_prefix",default="http://mitra.stanford.edu/kundaje/projects/GECCO/") 
    parser.add_argument("--prefix_to_drop_for_oak",default="/oak/stanford/groups/akundaje/projects/GECCO/")
 
    return parser.parse_args() 
def main(): 
    args=parse_args() 
    sample_to_files=dict() 
    pval_bigwigs=open(args.pval_bigwigs,'r').read().strip().split('\n') 
    fc_bigwigs=open(args.fc_bigwigs,'r').read().strip().split('\n')
    hammocks=open(args.hammocks,'r').read().strip().split('\n')
    num_samples=len(pval_bigwigs)
    fc_bigwig_json=[] 
    pval_bigwig_json=[] 

    for i in range(num_samples):
        fc_entry=fc_bigwigs[i].split('\t')
        fc_fname=fc_entry[0]
        fc_sample=fc_entry[1]

        pval_entry=pval_bigwigs[i].split('\t') 
        pval_fname=pval_entry[0]
        pval_sample=pval_entry[1]
        hammock_entry=hammocks[i].split('\t') 
        hammock_fname=hammock_entry[0]
        hammock_sample=hammock_entry[1]
        print(hammock_sample)
        assert fc_sample==hammock_sample
        print("-----") 
        print(fc_sample)
        print(pval_sample)
        
        print("-----") 
        assert fc_sample==pval_sample 
        

        #all samples the same
        sample=fc_sample
        print(sample) 


        fc_bigwig_dict={"type":"bigwig",
                        "url":fc_fname.replace(args.prefix_to_drop_for_oak,args.mitra_prefix),
                        "mode":1,
                        "name":",".join([sample,"FC"]),
                        "qtc": {"anglescale":1,
                                "pr":0,
                                "pg":0,
                                "pb":255,
                                "nr":0,
                                "ng":0,
                                "nb":255,
                                "pth":"rgb(0,0,178)",
                                "nth":"#800000",
                                "thtype":1,
                                "thmin":0,
                                "thmax":25,
                                "thpercentile":90,
                                "height":50,
                                "summeth":1}}
        pval_bigwig_dict={"type":"bigwig",
                        "url":pval_fname.replace(args.prefix_to_drop_for_oak,args.mitra_prefix),
                        "mode":1,
                        "name":",".join([sample,"PVAL"]),
                        "qtc": {"anglescale":1,
                                "pr":0,
                                "pg":0,
                                "pb":255,
                                "nr":0,
                                "ng":0,
                                "nb":255,
                                "pth":"rgb(0,0,178)",
                                "nth":"#800000",
                                "thtype":1,
                                "thmin":0,
                                "thmax":25,
                                "thpercentile":90,
                                "height":50,
                                "summeth":1}}
        
        hammock_dict={"type":"hammock",
                      "url":hammock_fname.replace(args.prefix_to_drop_for_oak,args.mitra_prefix),
                      "mode":3,
                      "name":",".join([sample,"HAMMOCK"])}
        fc_bigwig_json.append(fc_bigwig_dict)
        fc_bigwig_json.append(hammock_dict)
        pval_bigwig_json.append(pval_bigwig_dict)
        pval_bigwig_json.append(hammock_dict)
    with open(args.outf_fc_bigwig, 'w') as outfile:  
        json.dump(fc_bigwig_json, outfile)
    with open(args.outf_pval_bigwig,'w') as outfile: 
        json.dump(pval_bigwig_json,outfile) 
    
if __name__=="__main__": 
    main() 
