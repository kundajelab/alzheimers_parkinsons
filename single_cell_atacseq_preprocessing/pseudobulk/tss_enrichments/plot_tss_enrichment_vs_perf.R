rm(list=ls())
source("~/helpers.R")
library(ggplot2)
data=read.table("cluster.perf.means.vs.tss.txt",header=TRUE,sep='\t')
attach(data)
p1=ggplot(data=data,aes(x=TSSenrichment,y=spearmanr_nonzerobins,label=Cluster))+
  geom_point()+
  geom_text(nudge_y=0.01)+
  xlab("TSS Enrichment")+
  ylab("Spearman R non-zero bins")+
  theme_bw()

p2=ggplot(data=data,aes(x=TSSenrichment,y=pearsonr_nonzerobins,label=Cluster))+
  geom_point()+
  geom_text(nudge_y=0.01)+
  xlab("TSS Enrichment")+
  ylab("Pearson R non-zero bins")+
  theme_bw()

p3=ggplot(data=data,aes(x=TSSenrichment,y=spearmanr,label=Cluster))+
  geom_point()+
  geom_text(nudge_y=0.01)+
  xlab("TSS Enrichment")+
  ylab("Spearman R ")+
  theme_bw()

p4=ggplot(data=data,aes(x=TSSenrichment,y=pearsonr,label=Cluster))+
  geom_point()+
  geom_text(nudge_y=0.01)+
  xlab("TSS Enrichment")+
  ylab("Pearson R ")+
  theme_bw()

p5=ggplot(data=data,aes(x=TSSenrichment,y=auroc,label=Cluster))+
  geom_point()+
  geom_text(nudge_y=0.001)+
  xlab("TSS Enrichment")+
  ylab("auROC ")+
  theme_bw()

p6=ggplot(data=data,aes(x=TSSenrichment,y=auprc,label=Cluster))+
  geom_point()+
  geom_text(nudge_y=0.01)+
  xlab("TSS Enrichment")+
  ylab("auPRC")+
  theme_bw()

multiplot(p1,p2,p3,p4,p5,p6,cols=3)

