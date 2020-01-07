rm(list=ls())
library(ggplot2)
data=read.table("class.imbalance.txt",header=TRUE,sep='\t')
data$Cluster=factor(data$Cluster,levels=c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24))

p1=ggplot(data=data,
       aes(x=data$Cluster,y=data$NegPosRatio))+
  geom_boxplot()+
  xlab("Cluster")+
  ylab("Test Set: (# Negatives)/(# Positives)")+
  theme_bw(20) 
p2=ggplot(data=data,
          aes(x=data$Cluster,y=data$Pos))+
  geom_boxplot()+
  xlab("Cluster")+
  ylab("Test Set: # Positives")+
  theme_bw(20)

