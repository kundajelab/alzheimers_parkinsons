rm(list=ls())
library(ggplot2)
ctrl_counts=read.table("ctr.idr.optimal_set.sorted.merged.bed",header=FALSE,sep='\t')
ctrl_counts$length=ctrl_counts$V3-ctrl_counts$V2

p1=ggplot(data=ctrl_counts,aes(x=ctrl_counts$length))+
  geom_histogram(bins=100)+
  xlab("Peak Length")+
  ylab("Number of Peaks")+
  ggtitle("Control samples")+
  xlim(150,1000)
source("~/helpers.R")
multiplot(p1,cols=1)
