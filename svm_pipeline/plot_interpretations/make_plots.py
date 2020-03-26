import argparse
import numpy as np
import pickle
from dragonn.vis import *
from kerasAC.splits import * 
import pdb

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("--snpinfo")
    parser.add_argument("--tasks",nargs="+")
    parser.add_argument("--gkmexplain_pickle_prefix")
    parser.add_argument("--gkmexplain_pickle_suffix")    
    parser.add_argument("--deepshap_pickle_classification_prefix")
    parser.add_argument("--deepshap_pickle_regression_prefix")
    parser.add_argument("--outf_prefix")
    parser.add_argument("--plot_start_base",type=int,default=450)
    parser.add_argument("--plot_end_base",type=int,default=550)
    parser.add_argument("--snp_pos",type=int,default=501)    
    return parser.parse_args()

def plot_seq_importance(outf,tracks,labels,ylim,xlim,snp_pos, heatmap_indices=None, figsize=(10, 10)):
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 10}
    matplotlib.rc('font', **font)
    num_plots=len(tracks)
    f,axes=plt.subplots(num_plots,dpi=80,figsize=figsize)
    show=False
    seq_len = tracks[0].shape[0]
    hmaps={}
    for plot_index in range(num_plots): 
        cur_track=tracks[plot_index]
        cur_snp_pos=snp_pos[plot_index]
        cur_ylim=ylim[plot_index]
        cur_xlim=xlim[plot_index]
        vmin=-1*max([abs(cur_ylim[0]),abs(cur_ylim[1])])
        vmax=max([abs(cur_ylim[0]),abs(cur_ylim[1])])
        if (heatmap_indices is not None) and (plot_index in heatmap_indices):
            extent=[cur_xlim[0],cur_xlim[1],0,400]
            hmap=axes[plot_index].imshow(cur_track[cur_xlim[0]:cur_xlim[1],:].T,extent=extent,vmin=vmin,vmax=vmax,interpolation='nearest',aspect='auto',cmap='seismic')
            hmaps[plot_index]=hmap
            axes[plot_index].set_yticks(np.array([100,200,300,400]))
            axes[plot_index].set_yticklabels(['T','G','C','A'])
        else: 
            axes[plot_index]=plot_bases_on_ax(cur_track,axes[plot_index],show_ticks=True)
            axes[plot_index].set_xlim(cur_xlim) 
            axes[plot_index].set_ylim(cur_ylim)
        cur_label=labels[plot_index] 
        axes[plot_index].set_title(cur_label)
        axes[plot_index].axvline(x=cur_snp_pos,color='k',linestyle='--')
        axes[plot_index].tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off
    for hmap_index in hmaps:
        plt.colorbar(hmaps[hmap_index],ax=axes[hmap_index],orientation='horizontal')
    plt.subplots_adjust(hspace=0.5)
    plt.tight_layout()
    plt.savefig(outf,format='png',dpi=120)
    plt.close() 
    return 


def main():
    args=parse_args()
    #load the gkmexplain data
    snps=open(args.snpinfo,'r').read().strip().split('\n')
    for line in snps:
        print(line)
        snp_info=tuple(line.split('\t'))
        chrom=snp_info[0]
        fold_to_use=None
        for fold in hg19_splits:
            if chrom in hg19_splits[fold]['test']:
                fold_to_use=fold
                break
        assert fold_to_use is not None
        for task in args.tasks:
            print(str(snp_info)+":"+task+":"+str(fold_to_use))
            plot_wrapper(snp_info,fold_to_use,task,args)
    
def plot_wrapper(snp_info,fold_to_use,task,args):    
    rsid=snp_info[-1]
    gkmexplain_data=pickle.load(open(args.gkmexplain_pickle_prefix+task+args.gkmexplain_pickle_suffix,'rb'))
    mean_ref_gkmexplain=np.squeeze(gkmexplain_data[0][snp_info][0])
    mean_alt_gkmexplain=np.squeeze(gkmexplain_data[1][snp_info][0])
    delta_track=np.squeeze(gkmexplain_data[2][snp_info])
    ref_seqs=np.squeeze(gkmexplain_data[3][snp_info])
    alt_seqs=np.squeeze(gkmexplain_data[4][snp_info])
    delta_seqs=ref_seqs+alt_seqs

    #scale by input for plotting

    gkmexplain_scaled_ref=mean_ref_gkmexplain*ref_seqs
    gkmexplain_scaled_alt=mean_alt_gkmexplain*alt_seqs
    gkmexplain_scaled_delta=delta_track*delta_seqs
        
    #load deepshap ref classification
    deepshap_ref_data_class=np.load(args.deepshap_pickle_classification_prefix+str(fold_to_use)+'.'+task+'.ref.npz')
    rsids_ref_class=deepshap_ref_data_class['bed_entries']
    snp_index=rsids_ref_class.tolist().index(rsid)
    
    deepshap_ref_class=np.squeeze(deepshap_ref_data_class['interp_scores'][snp_index])
    deepshap_inputs_ref_class=np.squeeze(deepshap_ref_data_class['inputs_onehot'][snp_index])
    deepshap_scaled_ref_class=deepshap_ref_class*deepshap_inputs_ref_class
        
    #load deepshap alt classification
    deepshap_alt_data_class=np.load(args.deepshap_pickle_classification_prefix+str(fold_to_use)+'.'+task+'.alt.npz')
    rsids_alt_class=deepshap_alt_data_class['bed_entries']
    assert rsids_alt_class[snp_index]==rsid    
    deepshap_alt_class=np.squeeze(deepshap_alt_data_class['interp_scores'][snp_index])
    deepshap_inputs_alt_class=np.squeeze(deepshap_alt_data_class['inputs_onehot'][snp_index])
    deepshap_scaled_alt_class=deepshap_alt_class*deepshap_inputs_alt_class

    #get deepshap delta track classification
    deepshap_scaled_delta_class=(deepshap_alt_class - deepshap_ref_class)*(deepshap_inputs_alt_class+deepshap_inputs_ref_class)
    
    #load deepshap ref regression
    deepshap_ref_data_reg=np.load(args.deepshap_pickle_regression_prefix+str(fold_to_use)+'.'+task+'.ref.npz')
    rsids_ref_reg=deepshap_ref_data_reg['bed_entries']
    assert rsids_ref_reg[snp_index]==rsid
    deepshap_ref_reg=np.squeeze(deepshap_ref_data_reg['interp_scores'][snp_index])
    deepshap_inputs_ref_reg=np.squeeze(deepshap_ref_data_reg['inputs_onehot'][snp_index])
    deepshap_scaled_ref_reg=deepshap_ref_reg*deepshap_inputs_ref_reg

    #load deepshap alt regression
    deepshap_alt_data_reg=np.load(args.deepshap_pickle_regression_prefix+str(fold_to_use)+'.'+task+'.alt.npz')
    rsids_alt_reg=deepshap_alt_data_reg['bed_entries']
    assert rsids_alt_reg[snp_index]==rsid    
    deepshap_alt_reg=np.squeeze(deepshap_alt_data_reg['interp_scores'][snp_index])
    deepshap_inputs_alt_reg=np.squeeze(deepshap_alt_data_reg['inputs_onehot'][snp_index])
    deepshap_scaled_alt_reg=deepshap_alt_reg*deepshap_inputs_alt_reg

    #get deepshap delta track regression
    deepshap_scaled_delta_reg=(deepshap_alt_reg - deepshap_ref_reg)*(deepshap_inputs_alt_reg+deepshap_inputs_ref_reg)

    toplot_tracks=[gkmexplain_scaled_ref,
                   gkmexplain_scaled_alt,
                   gkmexplain_scaled_delta,
                   deepshap_scaled_ref_class,
                   deepshap_scaled_alt_class,
                   deepshap_scaled_delta_class,
                   deepshap_scaled_ref_reg,
                   deepshap_scaled_alt_reg,
                   deepshap_scaled_delta_reg]
    minvals=[]
    maxvals=[]
    
    #gkm y bounds 
    gkm_min=min([np.amin(i) for i in [gkmexplain_scaled_ref, gkmexplain_scaled_alt, gkmexplain_scaled_delta]])
    minvals.append(gkm_min)
    minvals.append(gkm_min)
    minvals.append(gkm_min)
    gkm_max=max([np.amax(i) for i in [gkmexplain_scaled_ref, gkmexplain_scaled_alt, gkmexplain_scaled_delta]])
    maxvals.append(gkm_max)
    maxvals.append(gkm_max)
    maxvals.append(gkm_max)

    #deepshap classification y bounds
    deepshap_class_min=min([np.amin(i) for i in [deepshap_scaled_ref_class, deepshap_scaled_alt_class, deepshap_scaled_delta_class]])
    minvals.append(deepshap_class_min)
    minvals.append(deepshap_class_min)
    minvals.append(deepshap_class_min)
    deepshap_class_max=max([np.amax(i) for i in [deepshap_scaled_ref_class, deepshap_scaled_alt_class, deepshap_scaled_delta_class]])
    maxvals.append(deepshap_class_max)
    maxvals.append(deepshap_class_max)
    maxvals.append(deepshap_class_max)

    #deepshap regression y bounds
    deepshap_reg_min=min([np.amin(i) for i in [deepshap_scaled_ref_reg, deepshap_scaled_alt_reg, deepshap_scaled_delta_reg]])
    minvals.append(deepshap_reg_min)
    minvals.append(deepshap_reg_min)
    minvals.append(deepshap_reg_min)
    deepshap_reg_max=max([np.amax(i) for i in [deepshap_scaled_ref_reg, deepshap_scaled_alt_reg, deepshap_scaled_delta_reg]])
    maxvals.append(deepshap_reg_max)
    maxvals.append(deepshap_reg_max)
    maxvals.append(deepshap_reg_max)


    ylim=[(minvals[i],maxvals[i]) for i in range(len(toplot_tracks))]
    xlim=[(args.plot_start_base,args.plot_end_base) for i in range(len(toplot_tracks))]
          
    toplot_labels=[rsid+' '+task+' GKMexplain ref:'+snp_info[2],
                   rsid+' '+task+' GKMexplain alt:'+snp_info[3],
                   rsid+' '+task+' GKMexplain alt - ref',
                   rsid+' '+task+' fold:'+str(fold_to_use)+' DeepSHAP ref class. :'+snp_info[2],
                   rsid+' '+task+' fold:'+str(fold_to_use)+' DeepSHAP alt class. :'+snp_info[3],
                   rsid+' '+task+' fold:'+str(fold_to_use)+' DeepSHAP alt - ref class.',
                   rsid+' '+task+' fold:'+str(fold_to_use)+' DeepSHAP ref reg. :'+snp_info[2],
                   rsid+' '+task+' fold:'+str(fold_to_use)+' DeepSHAP alt reg. :'+snp_info[3],
                   rsid+' '+task+' fold:'+str(fold_to_use)+' DeepSHAP alt - ref reg.']
    snp_pos=[args.snp_pos for i in range(len(toplot_tracks))]
    plot_seq_importance(args.outf_prefix+'/'+rsid+'/'+task+'.'+rsid+'.'+str(fold_to_use)+'.png',
                        toplot_tracks,
                        toplot_labels,
                        ylim=ylim,
                        xlim=xlim,
                        snp_pos=snp_pos,
                        heatmap_indices=None)
    
if __name__=="__main__":
    main()
    
