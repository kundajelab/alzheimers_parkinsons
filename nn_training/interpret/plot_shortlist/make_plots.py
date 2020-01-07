#generate plots for snps
import argparse
import pickle
from dragonn.vis import *
import os.path


def parse_args():
    parser=argparse.ArgumentParser(description="generate plots for ADPD SNPs")
    parser.add_argument("--input_pickle_classification")
    parser.add_argument("--input_pickle_regression")
    parser.add_argument("--cluster") 
    parser.add_argument("--fold") 
    parser.add_argument("--outpng_prefix",default="")
    return parser.parse_args()


def plot_seq_importance(tracks,labels,ylim, heatmap_indices=None, xlim=None, figsize=(25, 6),title="",snp_pos=0):
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}
    matplotlib.rc('font', **font)
    num_plots=len(tracks)
    f,axes=plt.subplots(num_plots,dpi=80,figsize=figsize)
    show=False
    tracks=[i.squeeze() for i in tracks] 
    seq_len = tracks[0].shape[0]
    hmaps={}
    if xlim is None:
        xlim = (0, seq_len)
    for plot_index in range(num_plots): 
        cur_track=tracks[plot_index]
        if (heatmap_indices is not None) and (plot_index in heatmap_indices):
            extent=[xlim[0],xlim[1],0,400]
            hmap=axes[plot_index].imshow(cur_track[xlim[0]:xlim[1],:].T,extent=extent,vmin=ylim[plot_index][0],vmax=ylim[plot_index][1],interpolation='nearest',aspect='auto',cmap='seismic')
            hmaps[plot_index]=hmap
            axes[plot_index].set_yticks(np.array([100,200,300,400]))
            axes[plot_index].set_yticklabels(['T','G','C','A'])
        else: 
            axes[plot_index]=plot_bases_on_ax(cur_track,axes[plot_index],show_ticks=True)
            axes[plot_index].set_xlim(xlim) 
            axes[plot_index].set_ylim(ylim[plot_index])
        cur_label=labels[plot_index] 
        axes[plot_index].set_title(cur_label)
        axes[plot_index].axvline(x=snp_pos,color='k',linestyle='--')
        axes[plot_index].tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off
    for hmap_index in hmaps:
        plt.colorbar(hmaps[hmap_index],ax=axes[hmap_index],orientation='horizontal')
    plt.subplots_adjust(hspace=0.8)
    plt.tight_layout()
    plt.savefig(title,format='svg',dpi=120)
    plt.close() 
    return 


def main():
    args=parse_args()
    #load the input pickle
    classification=pickle.load(open(args.input_pickle_classification,'rb'))
    print("loaded classification pickle") 
    regression=pickle.load(open(args.input_pickle_regression,'rb'))
    print("loaded regression pickle")
    snps=classification['rsid']
    class_gradxinput_ref=classification['gradxinput_ref']
    class_gradxinput_alt=classification['gradxinput_alt']
    class_gradxinput_delta=classification['gradxinput_delta']
    class_ism=classification['ism']
    class_ismxinput=classification['ismxinput']
    reg_gradxinput_ref=regression['gradxinput_ref']
    reg_gradxinput_alt=regression['gradxinput_alt']
    reg_gradxinput_delta=regression['gradxinput_delta']
    reg_ism=regression['ism']
    reg_ismxinput=regression['ismxinput']
    print("plotting...")
    for index in range(len(snps)):
        cur_snp=snps[index]
        print(cur_snp)
        cur_title='.'.join([cur_snp,args.cluster,args.fold,'svg'])
        if os.path.isfile(cur_title):
            continue

        #make the plot for the current snp
        '''
        cur_tracks=[class_gradxinput_ref[index],
                    class_gradxinput_alt[index],
                    class_gradxinput_delta[index],
                    reg_gradxinput_ref[index],
                    reg_gradxinput_alt[index],
                    reg_gradxinput_delta[index], 
                    class_ismxinput[index],
                    class_ism[index],
                    reg_ismxinput[index],
                    reg_ism[index]]
        '''
        cur_tracks=[
            class_ismxinput[index],
            class_ism[index],
            reg_ismxinput[index],
            reg_ism[index]]

        minvals=[]
        maxvals=[]
        '''
        classification y bounds
        class_min=min([np.amin(i) for i in [class_gradxinput_ref[index],class_gradxinput_alt[index],class_gradxinput_delta[index]]])
        minvals.append(class_min)
        minvals.append(class_min)
        minvals.append(class_min)
        class_max=max([np.amax(i) for i in [class_gradxinput_ref[index],class_gradxinput_alt[index],class_gradxinput_delta[index]]])        
        maxvals.append(class_max)
        maxvals.append(class_max)
        maxvals.append(class_max)
        
        
        #regression y bounds
        reg_min=min([np.amin(i) for i in [reg_gradxinput_ref[index],reg_gradxinput_alt[index],reg_gradxinput_delta[index]]])
        minvals.append(reg_min)
        minvals.append(reg_min)
        minvals.append(reg_min)
        reg_max=max([np.amax(i) for i in [reg_gradxinput_ref[index],reg_gradxinput_alt[index],reg_gradxinput_delta[index]]])        
        maxvals.append(reg_max)
        maxvals.append(reg_max)
        maxvals.append(reg_max)
        '''                
        #ism classification y bounds
        minvals.append(np.amin(class_ismxinput[index]))
        maxvals.append(np.amax(class_ismxinput[index]))
        minvals.append(np.amin(class_ismxinput[index]))
        maxvals.append(np.amax(class_ismxinput[index]))

        #ism regression y bounds
        minvals.append(np.amin(reg_ismxinput[index]))
        maxvals.append(np.amax(reg_ismxinput[index]))
        minvals.append(np.amin(reg_ismxinput[index]))
        maxvals.append(np.amax(reg_ismxinput[index]))

        ylim=[(minvals[i],maxvals[i]) for i in range(len(cur_tracks))]        
        cur_labels=[]
        '''
        cur_labels.append(':'.join([cur_snp,args.cluster,args.fold,'classification','gradxinput','noneffect']))
        cur_labels.append(':'.join([cur_snp,args.cluster,args.fold,'classification','gradxinput','effect']))
        cur_labels.append(':'.join([cur_snp,args.cluster,args.fold,'classification','gradxinput','effect - noneffect']))
        cur_labels.append(':'.join([cur_snp,args.cluster,args.fold,'regression','gradxinput','noneffect']))
        cur_labels.append(':'.join([cur_snp,args.cluster,args.fold,'regression','gradxinput','effect']))
        cur_labels.append(':'.join([cur_snp,args.cluster,args.fold,'regression','gradxinput','effect - noneffect']))
        '''
        cur_labels.append(':'.join([cur_snp,args.cluster,args.fold,'classification','ismxinput']))
        cur_labels.append(':'.join([cur_snp,args.cluster,args.fold,'classification','ism_heatmap']))
        cur_labels.append(':'.join([cur_snp,args.cluster,args.fold,'regression','ismxinput']))
        cur_labels.append(':'.join([cur_snp,args.cluster,args.fold,'regression','ism_heatmap']))
        plot_seq_importance(cur_tracks,
                            cur_labels, 
                            xlim=(400,600),
                            ylim=ylim,
                            heatmap_indices=[1,3],
                            figsize=(12,8),title=cur_title,
                            snp_pos=501)
if __name__=="__main__":
    main()
    
