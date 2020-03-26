import argparse
import pandas as pd
import numpy as np
import pickle
from dragonn.vis import *
from kerasAC.splits import * 
import pdb

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("--snpinfo")
    parser.add_argument("--tasks",nargs="+")
    parser.add_argument("--gkmexplain_prefix")
    parser.add_argument("--gkmexplain_suffix")    
    parser.add_argument("--deepshap_pickle_classification_prefix")
    parser.add_argument("--deepshap_pickle_regression_prefix")
    parser.add_argument("--outf_prefix")
    parser.add_argument("--plot_start_base",type=int,default=450)
    parser.add_argument("--plot_end_base",type=int,default=550)
    parser.add_argument("--snp_pos",type=int,default=501)    
    return parser.parse_args()

def plot_seq_importance(title,tracks,labels,ylim,xlim,snp_pos, heatmaps, figsize=(20,15)):
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 8}
    matplotlib.rc('font', **font)
    cols=len(tracks[0])
    rows=len(tracks)
    f,axes=plt.subplots(rows, cols,dpi=60,figsize=figsize)
    hmaps={}
    for row_index in range(rows):
        for col_index in range(cols):
            cur_track=tracks[row_index][col_index]
            cur_snp_pos=snp_pos[row_index][col_index]
            cur_ylim=ylim[row_index][col_index]
            cur_xlim=xlim[row_index][col_index]
            cur_label=labels[row_index][col_index]
            vmin=-1*max([abs(cur_ylim[0]),abs(cur_ylim[1])])
            vmax=max([abs(cur_ylim[0]),abs(cur_ylim[1])])
            print("row_index:"+str(row_index)+", col_index:"+str(col_index))
            is_heatmap=heatmaps[row_index][col_index]
            if is_heatmap is True:
                extent=[cur_xlim[0],cur_xlim[1],0,400]
                hmap=axes[row_index,col_index].imshow(cur_track[cur_xlim[0]:cur_xlim[1],:].T,extent=extent,vmin=vmin,vmax=vmax,interpolation='nearest',aspect='auto',cmap='seismic')
                hmaps[tuple([row_index,col_index])]=hmap
                axes[row_index,col_index].set_yticks(np.array([100,200,300,400]))
                axes[row_index,col_index].set_yticklabels(['T','G','C','A'])
            else: 
                axes[row_index,col_index]=plot_bases_on_ax(cur_track,axes[row_index,col_index],show_ticks=True)
                axes[row_index,col_index].set_xlim(cur_xlim) 
                axes[row_index,col_index].set_ylim(cur_ylim)
            axes[row_index,col_index].set_title(cur_label)
            axes[row_index,col_index].axvline(x=cur_snp_pos,color='k',linestyle='--')
            axes[row_index,col_index].tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                labelbottom=False) # labels along the bottom edge are off
    for hmap_index in hmaps:
        plt.colorbar(hmaps[hmap_index],ax=axes[hmap_index[0],hmap_index[1]],orientation='horizontal')
    plt.subplots_adjust(hspace=0.5)
    plt.tight_layout()
    plt.savefig(title,format='png',dpi=300)
    plt.close() 
    return 



def main():
    args=parse_args()
    #load the gkmexplain data
    snps=open(args.snpinfo,'r').read().strip().split('\n')
    for line in snps:
        print(line)
        snp_info=tuple(line.split('\t'))
        for task in args.tasks:
            plot_wrapper(snp_info,task,args)
    
def plot_wrapper(snp_info,task,args):    
    rsid=snp_info[-1]
    all_toplot_tracks=[]
    all_ylim=[]
    all_xlim=[]
    all_toplot_labels=[]
    all_snp_pos=[]
    all_heatmaps=[]    
    for fold in range(10):
        fold=str(fold)
        gkmexplain_ref=pd.read_csv(args.gkmexplain_prefix+'.ref'+'.'+task+'.'+fold+args.gkmexplain_suffix,sep='\t',header=None)
        for index,row in gkmexplain_ref.iterrows():
            label=row[0]
            if label=='_'.join(snp_info)+'_'+snp_info[2]:
                gkmexplain_ref=np.asarray([[float(j) for j in i.split(',')] for i in row[2].split(';')])
                break
        gkmexplain_alt=pd.read_csv(args.gkmexplain_prefix+'.alt'+'.'+task+'.'+fold+args.gkmexplain_suffix,sep='\t',header=None)
        for index,row in gkmexplain_alt.iterrows():
            label=row[0]
            if label=='_'.join(snp_info)+'_'+snp_info[3]:
                gkmexplain_alt=np.asarray([[float(j) for j in i.split(',')] for i in row[2].split(';')])
                break
        gkmexplain_delta=gkmexplain_alt-gkmexplain_ref
        

        #load deepshap ref classification
        deepshap_ref_data_class=np.load(args.deepshap_pickle_classification_prefix+str(fold)+'.'+task+'.ref.npz')
        rsids_ref_class=deepshap_ref_data_class['bed_entries']
        snp_index=rsids_ref_class.tolist().index(rsid)

        deepshap_ref_class=np.squeeze(deepshap_ref_data_class['interp_scores'][snp_index])
        deepshap_inputs_ref_class=np.squeeze(deepshap_ref_data_class['inputs_onehot'][snp_index])
        deepshap_scaled_ref_class=deepshap_ref_class*deepshap_inputs_ref_class

        #load deepshap alt classification
        deepshap_alt_data_class=np.load(args.deepshap_pickle_classification_prefix+str(fold)+'.'+task+'.alt.npz')
        rsids_alt_class=deepshap_alt_data_class['bed_entries']
        assert rsids_alt_class[snp_index]==rsid    
        deepshap_alt_class=np.squeeze(deepshap_alt_data_class['interp_scores'][snp_index])
        deepshap_inputs_alt_class=np.squeeze(deepshap_alt_data_class['inputs_onehot'][snp_index])
        deepshap_scaled_alt_class=deepshap_alt_class*deepshap_inputs_alt_class

        #get deepshap delta track classification
        deepshap_scaled_delta_class=(deepshap_alt_class - deepshap_ref_class)*(deepshap_inputs_alt_class+deepshap_inputs_ref_class)

        #load deepshap ref regression
        deepshap_ref_data_reg=np.load(args.deepshap_pickle_regression_prefix+str(fold)+'.'+task+'.ref.npz')
        rsids_ref_reg=deepshap_ref_data_reg['bed_entries']
        assert rsids_ref_reg[snp_index]==rsid
        deepshap_ref_reg=np.squeeze(deepshap_ref_data_reg['interp_scores'][snp_index])
        deepshap_inputs_ref_reg=np.squeeze(deepshap_ref_data_reg['inputs_onehot'][snp_index])
        deepshap_scaled_ref_reg=deepshap_ref_reg*deepshap_inputs_ref_reg

        #load deepshap alt regression
        deepshap_alt_data_reg=np.load(args.deepshap_pickle_regression_prefix+str(fold)+'.'+task+'.alt.npz')
        rsids_alt_reg=deepshap_alt_data_reg['bed_entries']
        assert rsids_alt_reg[snp_index]==rsid    
        deepshap_alt_reg=np.squeeze(deepshap_alt_data_reg['interp_scores'][snp_index])
        deepshap_inputs_alt_reg=np.squeeze(deepshap_alt_data_reg['inputs_onehot'][snp_index])
        deepshap_scaled_alt_reg=deepshap_alt_reg*deepshap_inputs_alt_reg

        #get deepshap delta track regression
        deepshap_scaled_delta_reg=(deepshap_alt_reg - deepshap_ref_reg)*(deepshap_inputs_alt_reg+deepshap_inputs_ref_reg)

        gkmexplain_scaled_delta=gkmexplain_delta*(deepshap_inputs_alt_reg+deepshap_inputs_ref_reg)
        
        toplot_tracks=[gkmexplain_scaled_delta,
                       deepshap_scaled_delta_class,
                       deepshap_scaled_delta_reg]
        all_toplot_tracks.append(toplot_tracks)
        
        minvals=3*[-.2]
        maxvals=3*[0.2]
        
        ylim=[(minvals[i],maxvals[i]) for i in range(len(toplot_tracks))]
        xlim=[(args.plot_start_base,args.plot_end_base) for i in range(len(toplot_tracks))]
        all_ylim.append(ylim)
        all_xlim.append(xlim)
        
        toplot_labels=[rsid+' '+task+' fold:'+str(fold)+' GKMexplain alt - ref',
                       rsid+' '+task+' fold:'+str(fold)+' DeepSHAP alt - ref class.',
                       rsid+' '+task+' fold:'+str(fold)+' DeepSHAP alt - ref reg.']
        all_toplot_labels.append(toplot_labels)
        
        snp_pos=[args.snp_pos for i in range(len(toplot_tracks))]
        all_snp_pos.append(snp_pos)

        heatmaps=[False,False,False]
        all_heatmaps.append(heatmaps)
    plot_seq_importance(args.outf_prefix+'/'+rsid+'/'+'folds'+'.'+task+'.'+rsid+'.png',
                        all_toplot_tracks,
                        all_toplot_labels,
                        ylim=all_ylim,
                        xlim=all_xlim,
                        snp_pos=all_snp_pos,
                        heatmaps=all_heatmaps)
    
if __name__=="__main__":
    main()
    
