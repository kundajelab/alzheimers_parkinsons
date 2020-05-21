rm(list=ls())
library(ggplot2)
source("~/helpers.R")
data=read.table("toplot.csv",header=TRUE,sep='\t')
p1=ggplot(data=data,aes(x=data$Region,y=data$N1))+geom_boxplot()+xlab("Brain Region (Bulk)")+ylab("N Peaks in Tech Rep 1")+theme_bw(15)
p2=ggplot(data=data,aes(x=data$Region,y=data$N2))+geom_boxplot()+xlab("Brain Region (Bulk)")+ylab("N Peaks in Tech Rep 2")+theme_bw(15)
multiplot(p1,p2,cols=1)

p3=ggplot(data=data,
          aes(x=data$SelfConsistencyRatio,
              group=data$Region,
              color=data$Region))+
  geom_density()+
  scale_color_manual(values=c('#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d'),name='Region')+xlab("Self Consistentcy Ratio")+ylab("Density")+theme_bw(20)
p4=ggplot(data=data,
          aes(x=data$RescueRatio,
              group=data$Region,
              color=data$Region))+
  geom_density()+
  scale_color_manual(values=c('#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d'),name='Region')+xlab("Rescue Ratio")+ylab("Density")+theme_bw(20)
multiplot(p3,p4,cols=2)
