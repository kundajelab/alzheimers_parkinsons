rm(list=ls())
library(ggplot2)
data=read.table('cluster.perf.txt',header=TRUE,sep='\t')
data$Cluster=factor(data$Cluster,levels=c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24))

auroc=data[data$Metric=='auroc',]
auprc=data[data$Metric=='auprc',]
spearman_nonzero=data[data$Metric=="spearmanr_nonzerobins",]
pearson_nonzero=data[data$Metric=='pearsonr_nonzerobins',]
spearmanr=data[data$Metric=="spearmanr",]
pearsonr=data[data$Metric=='pearsonr',]

p1=ggplot(data=auroc,aes(x=auroc$Cluster,y=auroc$Value))+geom_boxplot()+xlab('Cluster')+ylab('auROC')+ggtitle('GC corrected Classification')+theme_bw(20)
p2=ggplot(data=auprc,aes(x=auprc$Cluster,y=auprc$Value))+geom_boxplot()+xlab('Cluster')+ylab('auPRC')+ggtitle('GC corrected Classification')+theme_bw(20)
p3=ggplot(data=spearman_nonzero,aes(x=spearman_nonzero$Cluster,y=spearman_nonzero$Value))+geom_boxplot()+xlab('Cluster')+ylab('Spearman R (nonzero bins)')+ggtitle('GC Corrected Regression')+theme_bw(20)
p4=ggplot(data=pearson_nonzero,aes(x=pearson_nonzero$Cluster,y=pearson_nonzero$Value))+geom_boxplot()+xlab('Cluster')+ylab('Pearson R (nonzero bins)')+ggtitle('GC Corrected Regression')+theme_bw(20)
p5=ggplot(data=spearmanr,aes(x=spearmanr$Cluster,y=spearmanr$Value))+geom_boxplot()+xlab('Cluster')+ylab('Spearman R')+ggtitle('GC Corrected Regression')+theme_bw(20)
p6=ggplot(data=pearsonr,aes(x=pearsonr$Cluster,y=pearsonr$Value))+geom_boxplot()+xlab('Cluster')+ylab('Pearson R')+ggtitle('GC Corrected Regression')+theme_bw(20)
