
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
    parser.add_argument("--pickle_classification_dir",default="/srv/scratch/annashch/deeplearning/adpd/interpret/pickle_nn")
    parser.add_argument("--pickle_regression_dir",default="/srv/scratch/annashch/deeplearning/adpd/interpret/pickle_nn")
    parser.add_argument("--pickle_gkm_dir",default="/srv/scratch/annashch/deeplearning/adpd/interpret/aggregate_svm")    
    parser.add_argument("--cluster") 
    parser.add_argument("--snp")
    parser.add_argument("--effect_allele")
    parser.add_argument("--noneffect_allele") 
    parser.add_argument("--test_fold",type=int) 
    parser.add_argument("--nfolds",type=int,default=10)
    return parser.parse_args()


def plot_seq_importance(tracks,labels,ylim,xlim,snp_pos, heatmaps, figsize=(25, 6),title=""):
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 10}
    matplotlib.rc('font', **font)
    rows=len(tracks[0])
    cols=len(tracks)
    f,axes=plt.subplots(rows, cols,dpi=60,figsize=figsize)
    hmaps={}
    for row_index in range(rows):
        for col_index in range(cols):
            cur_track=tracks[col_index][row_index]
            cur_snp_pos=snp_pos[col_index]
            cur_ylim=ylim[col_index]
            cur_xlim=xlim[col_index]
            cur_label=labels[col_index][row_index]
            vmin=-1*max([abs(cur_ylim[0]),abs(cur_ylim[1])])
            vmax=max([abs(cur_ylim[0]),abs(cur_ylim[1])])
            print("col_index:"+str(col_index)+", row_index:"+str(row_index))
            is_heatmap=heatmaps[col_index][row_index]
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
    plt.savefig(title,format='svg',dpi=60)
    plt.close() 
    return 


def main():
    args=parse_args()

    #columns in plot:
    # 1) non-effect alleles gkm
    # 2) effect alleles gkm
    # 3) ism mat classification
    # 4) ismxinput classification
    # 5) ism mat regression
    # 6) ismxinput regression 
    tracks=[[] for i in range(6)]
    #plot labels 
    labels=[[] for i in range(6)]

    #is the plot a heatmap?
    heatmaps=[[False]*args.nfolds,[False]*args.nfolds,[True]*args.nfolds,[False]*args.nfolds,[True]*args.nfolds,[False]*args.nfolds]
    #establish the order of the folds with test fold on top 
    test_fold=args.test_fold
    folds=list(range(args.nfolds))
    folds.remove(test_fold)
    folds=[test_fold]+folds
    for fold in folds:
        #the fold is the row

        #load the corresponding fold tracks 
        classification=pickle.load(open(args.pickle_classification_dir+"/nn_unique.Cluster"+args.cluster+".fold"+str(fold)+".classification",'rb'))
        print("loaded classification pickle") 
        regression=pickle.load(open(args.pickle_classification_dir+"/nn_unique.Cluster"+args.cluster+".fold"+str(fold)+".regression",'rb'))
        print("loaded regression pickle")
        gkm=pickle.load(open(args.pickle_gkm_dir+"/gkm.Cluster"+args.cluster+".fold"+str(fold)+".pl",'rb'))
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
        
        tracks[0].append(gkm_noneffect)
        tracks[1].append(gkm_effect)
        tracks[2].append(class_ism)
        tracks[3].append(class_ismxinput)
        tracks[4].append(reg_ism)
        tracks[5].append(reg_ismxinput)
        #create labels for current folds
        labels[0].append(':'.join([args.snp,str(args.cluster),str(fold),"e/ne="+args.effect_allele+'/'+args.noneffect_allele,'gkmExplain','effect']))
        labels[1].append(':'.join([args.snp,str(args.cluster),str(fold),"e/ne="+args.effect_allele+'/'+args.noneffect_allele,'gkmExplain','non-effect']))
        labels[2].append(':'.join([args.snp,str(args.cluster),str(fold),"e/ne="+args.effect_allele+'/'+args.noneffect_allele,'classificationNN','ISM heatmap']))
        labels[3].append(':'.join([args.snp,str(args.cluster),str(fold),"e/ne="+args.effect_allele+'/'+args.noneffect_allele,'classificationNN','ISM x input']))
        labels[4].append(':'.join([args.snp,str(args.cluster),str(fold),"e/ne="+args.effect_allele+'/'+args.noneffect_allele,'regressionNN','ISM heatmap']))
        labels[5].append(':'.join([args.snp,str(args.cluster),str(fold),"e/ne="+args.effect_allele+'/'+args.noneffect_allele,'regressionNN','ISM x input']))

    for i in range(6):
        tracks[i]=[j.squeeze() for j in tracks[i]]
    print("plotting "+str(args.snp)+"...")
    cur_title='.'.join([args.snp,args.cluster+"_"+name_map[int(args.cluster)],"10folds",'svg'])

    minvals=[]
    maxvals=[]
    
    #gkm y bounds 
    gkm_min=min([np.amin(i) for i in tracks[0]+tracks[1]])
    minvals.append(gkm_min)
    minvals.append(gkm_min)
    gkm_max=max([np.amax(i) for i in tracks[0]+tracks[1]])
    maxvals.append(gkm_max)
    maxvals.append(gkm_max)

    #ism classification y bounds
    minvals.append(min([np.amin(i) for i in tracks[2]]))
    minvals.append(min([np.amin(i) for i in tracks[3]]))
    maxvals.append(max([np.amax(i) for i in tracks[2]]))
    maxvals.append(max([np.amax(i) for i in tracks[3]]))
    
    #ism regression y bounds
    minvals.append(min([np.amin(i) for i in tracks[4]]))
    minvals.append(min([np.amin(i) for i in tracks[5]]))
    maxvals.append(max([np.amax(i) for i in tracks[4]]))
    maxvals.append(max([np.amax(i) for i in tracks[5]]))


    ylim=[(minvals[i],maxvals[i]) for i in range(len(maxvals))]
    print(ylim) 
    #xlimits 
    xlim=[(399,599) for i in range(2)]+[(400,600) for i in range(4)]

    #snp pos 
    snp_pos=[500,500,501,501,501,501]
    
    
    
    
    plot_seq_importance(tracks,
                        labels, 
                        xlim=xlim,
                        ylim=ylim,
                        heatmaps=heatmaps,
                        figsize=(30,10),
                        title=cur_title,
                        snp_pos=snp_pos)
if __name__=="__main__":
    main()
    
