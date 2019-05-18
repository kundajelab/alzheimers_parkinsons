import json 
import argparse 
import pandas as pd 
import os 

def parse_args(): 
    parser=argparse.ArgumentParser(description="generate JSON inputs for running the pipeline starting w/ tagAligns")
    parser.add_argument("--target_dir",default="/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/merged_tagAligns_outputs") 
    parser.add_argument("--tagAlign_list",default="tagAligns.txt") 
    return parser.parse_args() 

def main(): 
    args=parse_args() 
    tagAligns=pd.read_table(args.tagAlign_list,header=None,sep='\t')

    for index,row in tagAligns.iterrows(): 

        #create the output directory if it doesn't exist 
        sample_dir='/'.join([args.target_dir,row[0]])
        try:
            os.stat(sample_dir)
        except:
            os.mkdir(sample_dir)

        #create the input json dictionary for the current sample 
        json_dict={} 
        json_dict['atac.pipeline_type']='atac' 
        json_dict['atac.genome.tsv']='/home/groups/cherry/encode/pipeline_genome_data/hg38_sherlock.tsv'
        json_dict['atac.paired_end']='true' 
        json_dict['atac.enable_idr']='true' 
        json_dict['atac.idr_thresh']=0.05 
        json_dict['atac.tas']=[row[1]]

        #dump to output file 
        out_string=json.dumps(json_dict, sort_keys=True, indent=4)
        outf=open('/'.join([sample_dir,row[0]+'.json']),'w')
        outf.write(out_string)
        outf.close() 


if __name__=="__main__": 
    main() 

