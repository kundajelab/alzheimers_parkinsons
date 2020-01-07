rm(list=ls())
library(ggplot2)
all_counts=read.table("idr.optimal_set.sorted.merged.bed",header=FALSE,sep='\t')
ctrl_counts=read.table("ctr.idr.optimal_set.sorted.merged.bed",header=FALSE,sep='\t')
all_counts$length=all_counts$V3-all_counts$V2
ctrl_counts$length=ctrl_counts$V3-ctrl_counts$V2
p1=ggplot(data=all_counts,aes(x=all_counts$length))+
  geom_histogram(bins=100)+
  xlab("Peak Length")+
  ylab("Number of Peaks")+
  ggtitle("All samples")+
  xlim(150,1000)
p2=ggplot(data=ctrl_counts,aes(x=ctrl_counts$length))+
  geom_histogram(bins=100)+
  xlab("Peak Length")+
  ylab("Number of Peaks")+
  ggtitle("Control samples")+
  xlim(150,1000)
source("~/helpers.R")
multiplot(p1,p2,cols=1)
