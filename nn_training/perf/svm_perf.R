rm(list=ls())
library(ggplot2)
library(reshape2)
#load the SVM data frame 
svm_auprc=read.table("auprc_scores.csv",header=TRUE,sep='\t')
svm_auroc=read.table("auroc_scores.csv",header=TRUE,sep='\t')
svm_auprc$cluster=factor(svm_auprc$cluster,levels=svm_auprc$cluster)
svm_auroc$cluster=factor(svm_auroc$cluster,levels=svm_auroc$cluster)

svm_auprc=melt(svm_auprc,id='cluster')
svm_auroc=melt(svm_auroc,id='cluster')

p1=ggplot(data=svm_auprc,
          aes(x=svm_auprc$cluster,
              y=svm_auprc$value))+
  geom_boxplot()+
  xlab("Cluster")+
  ylab("SVM auPRC")+
  theme_bw()+
  ylim(0.8,1.0)+
  theme(axis.text.x = element_text(angle = 90))

p2=ggplot(data=svm_auroc,
          aes(x=svm_auroc$cluster,
              y=svm_auroc$value))+
  geom_boxplot()+
  xlab("Cluster")+
  ylab("SVM auROC")+
  theme_bw()+
  ylim(0.8,1.0)+
  theme(axis.text.x = element_text(angle = 90))

source("~/helpers.R")
multiplot(p1,p2,cols=2)


