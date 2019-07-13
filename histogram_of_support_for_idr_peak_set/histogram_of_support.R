rm(list=ls())
library(ggplot2)
data=read.table("histogram_of_support.txt",header=TRUE,sep='\t')
ggplot(data=data,aes(x=data$NumSamples))+
  geom_histogram(bins=100)+
  xlab(" Number of supporting samples")+
  ylab("Number of Peaks")