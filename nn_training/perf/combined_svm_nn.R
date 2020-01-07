rm(list=ls())
library(ggplot2)
library(reshape2)
svm_auprc=read.table("auprc_scores.csv",header=TRUE,sep='\t')
svm_auroc=read.table("auroc_scores.csv",header=TRUE,sep='\t')
svm_auprc$cluster=factor(svm_auprc$cluster,levels=svm_auprc$cluster)
svm_auroc$cluster=factor(svm_auroc$cluster,levels=svm_auroc$cluster)

svm_auprc=melt(svm_auprc,id='cluster')
svm_auroc=melt(svm_auroc,id='cluster')
p1=ggplot(data=svm_auroc,
          aes(x=svm_auroc$cluster,
              y=svm_auroc$value))+
  geom_boxplot()+
  xlab("Cluster")+
  ylab("SVM auROC")+
  theme_bw()+
  ylim(0,1.0)+
  ggtitle("GkmSVM")+
  theme(axis.text.x = element_text(angle = 90))



p2=ggplot(data=svm_auprc,
          aes(x=svm_auprc$cluster,
              y=svm_auprc$value))+
  geom_boxplot()+
  xlab("Cluster")+
  ylab("SVM auPRC")+
  theme_bw()+
  ylim(0,1.0)+
  ggtitle("GkmSVM")+
  theme(axis.text.x = element_text(angle = 90))


data=read.table('cluster.perf.txt',header=TRUE,sep='\t')
data$Cluster=factor(data$Cluster,levels=c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24))

auroc=data[data$Metric=='auroc',]
auprc=data[data$Metric=='auprc',]
spearman_nonzero=data[data$Metric=="spearmanr_nonzerobins",]
pearson_nonzero=data[data$Metric=='pearsonr_nonzerobins',]
spearmanr=data[data$Metric=="spearmanr",]
pearsonr=data[data$Metric=='pearsonr',]

p3=ggplot(data=auroc,aes(x=auroc$Cluster,y=auroc$Value))+geom_boxplot()+xlab('Cluster')+ylab('auROC')+ggtitle('NN GC-corrected Classification')+theme_bw()+ylim(0,1.0)
p4=ggplot(data=auprc,aes(x=auprc$Cluster,y=auprc$Value))+geom_boxplot()+xlab('Cluster')+ylab('auPRC')+ggtitle('NN GC-corrected Classification')+theme_bw()+ylim(0,1.0)
p5=ggplot(data=spearman_nonzero,aes(x=spearman_nonzero$Cluster,y=spearman_nonzero$Value))+geom_boxplot()+xlab('Cluster')+ylab('Spearman R (nonzero bins)')+ggtitle('NN GC-corrected Regression')+theme_bw()+ylim(0,1.0)
p6=ggplot(data=pearson_nonzero,aes(x=pearson_nonzero$Cluster,y=pearson_nonzero$Value))+geom_boxplot()+xlab('Cluster')+ylab('Pearson R (nonzero bins)')+ggtitle('NN GC-corrected Regression')+theme_bw()+ylim(0,1.0)
p7=ggplot(data=spearmanr,aes(x=spearmanr$Cluster,y=spearmanr$Value))+geom_boxplot()+xlab('Cluster')+ylab('Spearman R')+ggtitle('NN GC-corrected Regression')+theme_bw()+ylim(0,1.0)
p8=ggplot(data=pearsonr,aes(x=pearsonr$Cluster,y=pearsonr$Value))+geom_boxplot()+xlab('Cluster')+ylab('Pearson R')+ggtitle('NN GC-corrected Regression')+theme_bw()+ylim(0,1.0)

source("~/helpers.R")
svg("combined_nn_svm_perf.svg",height=9,width=8)
multiplot(p1,p3,p5,p7,p2,p4,p6,p8,cols=2)
dev.off() 




