import argparse 
import json 
import pdb 

def parse_args(): 
    parser=argparse.ArgumentParser(description="aggregate ataqc metrics for all samples in a single report")
    parser.add_argument("--ataqc_files",default="/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/ataqc.json") 
    parser.add_argument("--outf",default="report.txt") 
    parser.add_argument("--mitra_prefix",default="http://mitra.stanford.edu/kundaje/projects/alzheimers_parkinsons/") 
    parser.add_argument("--prefix_to_drop_for_oak",default="/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/")
    return parser.parse_args() 

def get_frip(json_dict): 
    frip_macs2_qc=json_dict['frip_macs2_qc'] 
    frip_macs2_rep2=None 
    try: 
        frip_macs2_rep1=frip_macs2_qc['rep1']['FRiP'] 
    except: 
        frip_macs2_rep1=None 
    
    try: 
        frip_macs2_rep2=frip_macs2_qc['rep2']['FRiP'] 
    except: 
        frip_macs2_rep2=None 
    overlap_frip_qc=json_dict['overlap_frip_qc']
    idr_frip_qc=json_dict['idr_frip_qc'] 
    for key in overlap_frip_qc: 
        overlap_frip=overlap_frip_qc[key]['FRiP']
    for key in idr_frip_qc: 
        idr_frip=idr_frip_qc[key]['FRiP']
    out='\t'.join([str(i) for i in [frip_macs2_rep1,frip_macs2_rep2,overlap_frip,idr_frip]])
    return out 

def main(): 
    args=parse_args() 
    ataqc_files=open(args.ataqc_files,'r').read().strip().split('\n') 
    outf=open(args.outf,'w') 
    categories=['overlap_reproducibility_qc','idr_reproducibility_qc']
    metrics=['Nt','N1','N2','Np','N_opt','N_consv','opt_set','consv_set','rescue_ratio','self_consistency_ratio','reproducibility']
    outf.write('\t'.join(["PD/AD","Region","Condition","Sample","ATAQC_Report","FRiP_rep1","FRiP_rep2","FRiP_overlap","FRiP_idr"]))
    for category in categories: 
        for metric in metrics: 
            outf.write('\t'+'_'.join([metric,category]))
    outf.write('\n')
    for f in ataqc_files: 
        #get the mitra link for the html ataqc report 
        mitra_file_path=f.replace(args.prefix_to_drop_for_oak,args.mitra_prefix).replace('.json','.html')
        
        #determine if the sample is AD or PD 
        if f.__contains__("/outputs_PD/"): 
            dataset="PD" 
        else: 
            dataset="AD" 

        #get the sample name 
        tokens=f.split('/') 
        region=tokens[8] 
        condition=tokens[9] 
        sample_id=tokens[10] 
        try:
            data=json.load(open(f,'r')) 
        except: 
            print("could not load:"+str(f))
            continue 
        frip_metrics=get_frip(data)
        idr_reproducibility_qc=data['idr_reproducibility_qc'] 
        overlap_reproducibility_qc=data['overlap_reproducibility_qc'] 
        outf.write('\t'.join([dataset,region,condition,sample_id,mitra_file_path,frip_metrics]))
        for metric in metrics: 
            try:
                outf.write("\t"+str(overlap_reproducibility_qc[metric]))
            except: 
                outf.write("\tNull") 
        for metric in metrics: 
            try:
                outf.write("\t"+str(idr_reproducibility_qc[metric]))
            except: 
                outf.write("\tNull") 
        outf.write("\n") 

if __name__=="__main__": 
    main() 
