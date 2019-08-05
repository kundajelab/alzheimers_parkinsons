import json 
import argparse 
import pandas as pd 
import os 

def parse_args(): 
    parser=argparse.ArgumentParser(description="generate JSON inputs for running the pipeline starting w/ tagAligns")
    parser.add_argument("--json_dir",default="/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_jsons") 
    parser.add_argument("--tagAlign_list",default="tagAligns.txt")
    parser.add_argument("--genome_tsv_for_pipeline",default="/mnt/data/annotations/by_release/hg38_klab.tsv")
    parser.add_argument("--output_dir",default="/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs")  
    parser.add_argument("--caper_submit_script",default="/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/submit.sh")
    return parser.parse_args() 

def main(): 
    args=parse_args()

        #create the pipeline_json_dir if it doesn't exist yet, this is where all the jsons for the pipeline will be stored.
    if os.path.exists(args.json_dir) is False:
        os.makedirs(args.json_dir)

    if os.path.exists(args.output_dir) is False:
        os.makedirs(args.output_dir)

    tagAligns=pd.read_table(args.tagAlign_list,header=None,sep='\t')
    sample_to_json=dict() 
    for index,row in tagAligns.iterrows(): 
        #create the input json dictionary for the current sample 
        json_dict={} 
        json_dict['atac.pipeline_type']='atac' 
        json_dict['atac.genome.tsv']='/mnt/data/annotations/by_release/hg38_klab.tsv'
        json_dict['atac.paired_end']='true' 
        json_dict['atac.enable_idr']='true' 
        json_dict['atac.idr_thresh']=0.05 
        json_dict['atac.tas']=[row[1]]
        json_dict['atac.chrsz']="/mnt/data/annotations/by_release/hg38/hg38.chrom.sizes"
        json_dict['atac.gensz']='hs'
        json_dict['atac.xcor_cpu']=10
        json_dict['atac.blacklist']='/mnt/data/annotations/by_release/hg38/hg38.blacklist.bed.gz'
        json_dict['atac.fingerprint_cpu']=10
        #for some reason, these need to be specified explicitly when starting pipeline w/ tagAlign:
        json_dict['atac.ref_fa']="/mnt/data/pipeline_genome_data/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta.gz"
        json_dict['atac.tss']="/mnt/data/pipeline_genome_data/hg38/ataqc/hg38_gencode_tss_unique.bed.gz"
        json_dict['atac.dnase']="/mnt/data/pipeline_genome_data/hg38/ataqc/reg2map_honeybadger2_dnase_all_p10_ucsc.hg19_to_hg38.bed.gz"
        json_dict['atac.prom']="/mnt/data/pipeline_genome_data/hg38/ataqc/reg2map_honeybadger2_dnase_prom_p2.hg19_to_hg38.bed.gz"
        json_dict['atac.enh']="/mnt/data/pipeline_genome_data/hg38/ataqc/reg2map_honeybadger2_dnase_enh_p2.hg19_to_hg38.bed.gz"
        json_dict['atac.reg2map']="/mnt/data/pipeline_genome_data/hg38/ataqc/hg38_dnase_avg_fseq_signal_formatted.txt.gz"
        json_dict['atac.reg2map_bed']="/mnt/data/pipeline_genome_data/hg38/ataqc/hg38_celltype_compare_subsample.bed.gz"
        json_dict['atac.roadmap_meta']="/mnt/data/pipeline_genome_data/hg38/ataqc/hg38_dnase_avg_fseq_signal_metadata.txt"
         
        #dump to output file 
        out_string=json.dumps(json_dict, sort_keys=True, indent=4)
        json_path='/'.join([args.json_dir,row[0]+'.json'])
        outf=open(json_path,'w')
        outf.write(out_string)
        outf.close()
        sample_to_json[row[0]]=json_path
    #create the caper submit script
    with open(args.caper_submit_script,'w') as submit_f:
        submit_f.write('#!/bin/bash\n')
        submit_f.write('source activate encode-atac-seq-pipeline\n')
        for sample in sample_to_json:
            submit_f.write('caper submit ~/atac-seq-pipeline/atac.wdl -i '+sample_to_json[sample]+' -s '+sample+' --ip localhost --port 8000\n')    
if __name__=="__main__": 
    main() 

