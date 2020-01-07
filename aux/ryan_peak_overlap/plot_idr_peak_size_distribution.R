rm(list=ls())
library(ggplot2)
source("~/helpers.R")
data=read.table("idr.optimal_set.sorted.merged.bed",header=FALSE,sep='\t')
control=read.table("ctr.idr.optimal_set.sorted.merged.bed",header=FALSE,sep='\t')
data$peak_size=data$V3-data$V2
control$peak_size=control$V3-control$V2
p1=ggplot(data=data,aes(x=data$peak_size))+
  geom_density()+
  xlab("IDR merged peak size")+
  ylab("Number of Peaks")+
  xlim(0,2000)
p2=ggplot(data=control,aes(x=control$peak_size))+
  geom_density()+
  xlab("Controls IDR merged peak size")+
  ylab("Number of Peaks")+
  xlim(0,2000)
multiplot(p1,p2,cols=1)
p3=ggplot(data=data,aes(x=data$peak_size))+
  geom_histogram(bins=60)+
  xlab("IDR merged peak size")+
  ylab("Number of Peaks")+
  xlim(0,2000)
p4=ggplot(data=control,aes(x=control$peak_size))+
  geom_histogram(bins=60)+
  xlab("Controls IDR merged peak size")+
  ylab("Number of Peaks")+
  xlim(0,2000)
multiplot(p3,p4,cols=1)
