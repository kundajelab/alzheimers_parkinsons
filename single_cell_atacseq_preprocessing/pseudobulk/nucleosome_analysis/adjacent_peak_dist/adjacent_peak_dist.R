rm(list=ls())
library(ggplot2)
data=read.table("all_peak_dists.tsv",header=FALSE,sep='\t')
data=as.data.frame(data[data$V1<50000,])
names(data)=c("V1")
ggplot(data=data,
       aes(x=data$V1))+
  geom_histogram(bins=1000)+
  xlim(0,1000)+
  xlab("Distance between adjacent peaks on same chrom")+
  ylab("Number of peaks (combined across clusters)")+
  theme_bw(20)
