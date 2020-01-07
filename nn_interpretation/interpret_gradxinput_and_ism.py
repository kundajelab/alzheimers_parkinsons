import warnings
warnings.filterwarnings("ignore")
import argparse
import pdb
import pickle
from kerasAC.generators.snp_generator import *
from kerasAC.interpret.ism import *
from kerasAC.interpret import load_model 
from kerasAC.interpret import input_grad

def parse_args():
    parser=argparse.ArgumentParser(description="perform gradient x input interpretation on a set of snps")
    parser.add_argument("--bed_path",default="/srv/scratch/annashch/deeplearning/adpd/interpret/SigSNPs_AllClusters_MergedUnique.csv")
    parser.add_argument("--ref_allele_col",default="noneffect")
    parser.add_argument("--alt_allele_col",default="effect")
    parser.add_argument("--compute_gc",default=False,action="store_true")
    parser.add_argument("--flank_size",type=int,default=500)
    parser.add_argument("--chrom_col",default="chr")
    parser.add_argument("--pos_col",default="start")
    parser.add_argument("--rsid_col",default=None)
    parser.add_argument("--ref_fasta",default="/mnt/data/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta")
    parser.add_argument("--batch_size",type=int,default=100)
    parser.add_argument("--model_string")
    parser.add_argument("--target_layer_idx",type=int,default=-2,help="use -2 for classification model, -1 for regression model")
    parser.add_argument("--outf")
    
    return parser.parse_args()

def get_all_gradxinput(ref_gen,alt_gen,model,args):
    all_rsid=None
    all_gradxinput_ref=None
    all_gradxinput_alt=None
    all_gradxinput_delta=None 
    for batch_index in range(len(ref_gen)):
        batch_ref=ref_gen[batch_index]
        batch_alt=alt_gen[batch_index]
        batch_rsid=batch_ref[0]
        X_ref=batch_ref[1]
        X_alt=batch_alt[1] 
        grads_ref=input_grad(model,X_ref,target_layer_idx=args.target_layer_idx,input_to_use=0)
        grads_alt=input_grad(model,X_alt,target_layer_idx=args.target_layer_idx,input_to_use=0)
        grads_delta=grads_alt-grads_ref 
        gradxinput_ref=grads_ref*X_ref[0]
        gradxinput_alt=grads_alt*X_alt[0]
        gradxinput_delta=grads_delta*X_alt[0]
        
        if all_gradxinput_ref is None:
            all_gradxinput_ref=gradxinput_ref
            all_gradxinput_alt=gradxinput_alt
            all_gradxinput_delta=gradxinput_delta
            all_rsid=batch_rsid 
        else:
            all_gradxinput_ref=np.concatenate((all_gradxinput_ref,gradxinput_ref),axis=0)
            all_gradxinput_alt=np.concatenate((all_gradxinput_alt,gradxinput_alt),axis=0)
            all_gradxinput_delta=np.concatenate((all_gradxinput_delta,gradxinput_delta),axis=0)
            all_rsid=all_rsid+batch_rsid
    return all_gradxinput_ref,all_gradxinput_alt, all_gradxinput_delta,all_rsid

def get_all_ism(gen,model,args):
    all_ism=None
    all_ismxinput=None
    for batch in gen:
        X=batch[1]
        ism_vals,ism_vals_x_input=in_silico_mutagenesis_gc(model,X,0,target_layer_idx=args.target_layer_idx)
        if all_ism is None:
            all_ism=ism_vals
            all_ismxinput=ism_vals_x_input 
        else:
            all_ism=np.concatenate((all_ism,ism_vals),axis=0)
            all_ismxinput=np.concatenate((all_ismxinput,ism_vals_x_input),axis=0)            
    return all_ism,all_ismxinput


def main():
    args=parse_args()
    #create snp generators

    ref_gen=SNPGenerator(bed_path=args.bed_path,
             chrom_col=args.chrom_col,
             pos_col=args.pos_col,
             allele_col=args.ref_allele_col,
             flank_size=args.flank_size,
             rsid_col=args.rsid_col,
             compute_gc=args.compute_gc,
                     ref_fasta=args.ref_fasta,
                     batch_size=args.batch_size)
    print("Got ref allele generator!") 
    
    alt_gen=SNPGenerator(bed_path=args.bed_path,
                 chrom_col=args.chrom_col,
                 pos_col=args.pos_col,
                 allele_col=args.alt_allele_col,
                 flank_size=args.flank_size,
                 rsid_col=args.rsid_col,
                 compute_gc=args.compute_gc,
                         ref_fasta=args.ref_fasta,
                         batch_size=args.batch_size)
    print("Got alt allele generator!")
    
    #load the model
    model=load_model(args.model_string)
    print("loaded model")
    
    #compute gradxinput
    all_gradxinput_ref,all_gradxinput_alt, all_gradxinput_delta, all_rsid=get_all_gradxinput(ref_gen,alt_gen,model,args)
    
    #compute ism
    all_ism,all_ismxinput=get_all_ism(alt_gen,model,args)
    
    #store the outputs in a pickle
    outputs={'rsid':all_rsid,
             'gradxinput_ref':all_gradxinput_ref,
             'gradxinput_alt':all_gradxinput_alt,
             'gradxinput_delta':all_gradxinput_delta,
             'ism':all_ism,
             'ismxinput':all_ismxinput}
    pickle.dump(outputs,open(args.outf,'wb'))
    
if __name__=="__main__":
    main()
    
