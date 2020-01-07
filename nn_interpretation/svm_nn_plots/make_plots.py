#generate plots for snps
import argparse
import pickle
from dragonn.vis import *
import os.path
name_map={}
name_map[13]="astrocytes"
name_map[14]="astrocytes"
name_map[15]="astrocytes"
name_map[16]="astrocytes"
name_map[17]="astrocytes"
name_map[1]="excitatory_neurons"
name_map[3]="excitatory_neurons"
name_map[4]="excitatory_neurons"
name_map[11]="inhibitory_neurons"
name_map[12]="inhibitory_neurons"
name_map[2]="inhibitory_neurons"
name_map[24]="microglia"
name_map[19]="oligodendrocytes"
name_map[20]="oligodendrocytes"
name_map[21]="oligodendrocytes"
name_map[22]="oligodendrocytes"
name_map[23]="oligodendrocytes"
name_map[10]="opcs"
name_map[8]="opcs"
name_map[9]="opcs"
name_map[5]="nigral_neurons"
name_map[6]="nigral_neurons"
name_map[18]="doublets"
name_map[7]="unknown"


def parse_args():
    parser=argparse.ArgumentParser(description="generate plots for ADPD SNPs")
    parser.add_argument("--pickle_classification_dir",default="/srv/scratch/annashch/deeplearning/adpd/interpret/pickles_sig")
    parser.add_argument("--pickle_regression_dir",default="/srv/scratch/annashch/deeplearning/adpd/interpret/pickles_sig")
    parser.add_argument("--pickle_gkm_dir",default="/srv/scratch/annashch/deeplearning/adpd/interpret/aggregate_svm")    
    parser.add_argument("--cluster") 
    parser.add_argument("--fold")
    parser.add_argument("--snp")
    parser.add_argument("--effect_allele")
    parser.add_argument("--noneffect_allele") 

    return parser.parse_args()


def plot_seq_importance(tracks,labels,ylim,xlim,snp_pos, heatmap_indices=None, figsize=(25, 6),title=""):
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 10}
    matplotlib.rc('font', **font)
    num_plots=len(tracks)
    f,axes=plt.subplots(num_plots,dpi=80,figsize=figsize)
    show=False
    tracks=[i.squeeze() for i in tracks] 
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
    plt.savefig(title,format='svg',dpi=120)
    plt.close() 
    return 


def main():
    args=parse_args()
    #load the input pickle
    classification=pickle.load(open(args.pickle_classification_dir+"/sig.snps.Cluster"+args.cluster+".fold"+args.fold+".classification",'rb'))
    print("loaded classification pickle") 
    regression=pickle.load(open(args.pickle_classification_dir+"/sig.snps.Cluster"+args.cluster+".fold"+args.fold+".regression",'rb'))
    print("loaded regression pickle")
    gkm=pickle.load(open(args.pickle_gkm_dir+"/gkm.Cluster"+args.cluster+".fold"+args.fold+".pl",'rb'))
    print("loaded gkm pickle") 
    nn_snps=classification['rsid']
    nn_index=nn_snps.index(args.snp)
    class_ism=classification['ism'][nn_index] 
    class_ismxinput=classification['ismxinput'][nn_index]
    reg_ism=regression['ism'][nn_index]
    reg_ismxinput=regression['ismxinput'][nn_index]
    gkm_snps=gkm['rsid']
    try:

        gkm_index=gkm_snps.index(args.snp)
        gkm_effect=gkm['gkm_effect'][gkm_index]
        gkm_noneffect=gkm['gkm_noneffect'][gkm_index]
        gkm_delta=gkm['gkm_delta'][gkm_index]
    except:
        gkm_effect=np.zeros((1000,4))
        gkm_noneffect=np.zeros((1000,4))
        gkm_delta=np.zeros((1000,4))
        
    print("plotting "+str(args.snp)+"...")
    cur_title='.'.join([args.snp,args.cluster+"_"+name_map[int(args.cluster)],args.fold,'svg'])
    cur_tracks=[
        gkm_noneffect,
        gkm_effect,
        gkm_delta,
        class_ismxinput,
        class_ism,
        reg_ismxinput,
        reg_ism]

    minvals=[]
    maxvals=[]
    
    #gkm y bounds 
    gkm_min=min([np.amin(i) for i in [gkm_noneffect, gkm_effect, gkm_delta]])
    minvals.append(gkm_min)
    minvals.append(gkm_min)
    minvals.append(gkm_min)
    gkm_max=max([np.amax(i) for i in [gkm_noneffect, gkm_effect, gkm_delta]])
    maxvals.append(gkm_max)
    maxvals.append(gkm_max)
    maxvals.append(gkm_max)

    #ism classification y bounds
    minvals.append(np.amin(class_ismxinput))
    maxvals.append(np.amax(class_ismxinput))
    minvals.append(np.amin(class_ismxinput))
    maxvals.append(np.amax(class_ismxinput))

    #ism regression y bounds
    minvals.append(np.amin(reg_ismxinput))
    maxvals.append(np.amax(reg_ismxinput))
    minvals.append(np.amin(reg_ismxinput))
    maxvals.append(np.amax(reg_ismxinput))

    ylim=[(minvals[i],maxvals[i]) for i in range(len(cur_tracks))]

    #xlimits 
    xlim=[(399,599) for i in range(3)]+[(400,600) for i in range(4)]

    #snp pos 
    snp_pos=[500,500,500,501,501,501,501,501]
    
    #plot labels 
    cur_labels=[]
    cur_labels.append(':'.join([args.snp,args.cluster,args.fold,"e/ne="+args.effect_allele+'/'+args.noneffect_allele,'gkmExplain','non-effect']))
    cur_labels.append(':'.join([args.snp,args.cluster,args.fold,"e/ne="+args.effect_allele+'/'+args.noneffect_allele,'gkmExplain','effect']))
    cur_labels.append(':'.join([args.snp,args.cluster,args.fold,"e/ne="+args.effect_allele+'/'+args.noneffect_allele,'gkmExplain','effect - noneffect']))
    cur_labels.append(':'.join([args.snp,args.cluster,args.fold,"e/ne="+args.effect_allele+'/'+args.noneffect_allele,'classificationNN','ISM x input']))
    cur_labels.append(':'.join([args.snp,args.cluster,args.fold,"e/ne="+args.effect_allele+'/'+args.noneffect_allele,'classificationNN','ISM heatmap']))
    cur_labels.append(':'.join([args.snp,args.cluster,args.fold,"e/ne="+args.effect_allele+'/'+args.noneffect_allele,'regressionNN','ISM x input']))
    cur_labels.append(':'.join([args.snp,args.cluster,args.fold,"e/ne="+args.effect_allele+'/'+args.noneffect_allele,'regressionNN','ISM heatmap']))

    
    
    plot_seq_importance(cur_tracks,
                        cur_labels, 
                        xlim=xlim,
                        ylim=ylim,
                        heatmap_indices=[4,6],
                        figsize=(10,8),title=cur_title,
                        snp_pos=snp_pos)
if __name__=="__main__":
    main()
    
