data=read.table("fragment_length_aggregated_across_clusters.txt",header=FALSE,sep='\t')
library(ggplot2)
ggplot(data=data,aes(x=data$V1,y=data$V2))+
  geom_line()+
  xlab("Fragment Length")+
  ylab("Number of Fragments")+
  ggtitle("scATAC fragment length distribution")+
  xlim(0,1000)+
  theme_bw(20)