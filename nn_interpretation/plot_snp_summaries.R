rm(list=ls())
library(ggplot2)
classification=read.table('summaries.1.0.classification.txt',header=TRUE,sep='\t')
regression=read.table("summaries.1.0.regression.txt",header=TRUE,sep='\t')

d1=classification[order(classification$GradTotalSignal),]
d2=classification[order(classification$GradSignalRatio),]
d3=classification[order(classification$ISMTotalSignal),]
d4=classification[order(classification$ISMSignalRatio),]
d5=regression[order(regression$GradTotalSignal),]
d6=regression[order(regression$GradSignalRatio),]
d7=regression[order(regression$ISMTotalSignal),]
d8=regression[order(regression$ISMSignalRatio),]

p1=ggplot(data=d1,aes(x=seq(1,nrow(d1)),y=d1$GradTotalSignal,color=d1$SVMSig,size=d1$SVMSig))+
  geom_point(alpha=0.5)+
  scale_color_manual(values=c("#e41a1c","#377eb8"),name="SVM Significant?")+
  scale_size_manual(values=c(0.1,1),name="SVM Significant")+
  geom_hline(yintercept = 50.34)+
  ylab("class signal delta gradxinput")+
  xlab("SNP")+
  theme(legend.position = "none")

p2=ggplot(data=d2,aes(x=seq(1,nrow(d2)),y=d2$GradSignalRatio,color=d2$SVMSig,size=d2$SVMSig))+
  geom_point(alpha=0.5)+
  geom_hline(yintercept = 0.23)+
  scale_color_manual(values=c("#e41a1c","#377eb8"),name="SVM Significant?")+
  scale_size_manual(values=c(0.1,1),name="SVM Significant")+
  ylab("class signal ratio delta gradxinput")+
  xlab("SNP")+
  theme(legend.position = "none")


p3=ggplot(data=d3,aes(x=seq(1,nrow(d3)),y=d3$ISMTotalSignal,color=d3$SVMSig,size=d3$SVMSig))+
  geom_point(alpha=0.5)+
  geom_hline(yintercept = 147.32)+
  scale_color_manual(values=c("#e41a1c","#377eb8"),name="SVM Significant?")+
  scale_size_manual(values=c(0.1,1),name="SVM Significant")+
  ylab("class ISM 1kb signal")+
  xlab("class signal ISM")+
  theme(legend.position = "none")

p4=ggplot(data=d4,aes(x=seq(1,nrow(d4)),y=d4$ISMSignalRatio,color=d4$SVMSig,size=d4$SVMSig))+
  geom_point(alpha=0.5)+
  geom_hline(yintercept = 0.06)+
  scale_color_manual(values=c("#e41a1c","#377eb8"),name="SVM Significant?")+
  scale_size_manual(values=c(0.1,1),name="SVM Significant")+
  ylab("class signal ratio ISM")+
  xlab("SNP")+
  theme(legend.position = "none")

p5=ggplot(data=d5,aes(x=seq(1,nrow(d5)),y=d5$GradTotalSignal,color=d5$SVMSig,size=d5$SVMSig))+
  geom_point(alpha=0.5)+
  geom_hline(yintercept = 3.94)+
  scale_color_manual(values=c("#e41a1c","#377eb8"),name="SVM Significant?")+
  scale_size_manual(values=c(0.1,1),name="SVM Significant")+
  ylab("regress signal delta gradxinput")+
  xlab("SNP")+
  theme(legend.position = "none")

p6=ggplot(data=d6,aes(x=seq(1,nrow(d6)),y=d6$GradSignalRatio,color=d6$SVMSig,size=d6$SVMSig))+
  geom_point(alpha=0.5)+
  geom_hline(yintercept = 0.24)+
  scale_color_manual(values=c("#e41a1c","#377eb8"),name="SVM Significant?")+
  scale_size_manual(values=c(0.1,1),name="SVM Significant")+
  ylab("regress signal ratio delta gradxinput")+
  xlab("SNP")+
  theme(legend.position = "none")

p7=ggplot(data=d7,aes(x=seq(1,nrow(d7)),y=d7$ISMTotalSignal,color=d7$SVMSig,size=d7$SVMSig))+
  geom_point(alpha=0.5)+
  geom_hline(yintercept = 15.51)+
  scale_color_manual(values=c("#e41a1c","#377eb8"),name="SVM Significant?")+
  scale_size_manual(values=c(0.1,1),name="SVM Significant")+
  ylab("regress signal ISM")+
  xlab("SNP")+
  theme(legend.position = "none")

p8=ggplot(data=d8,aes(x=seq(1,nrow(d8)),y=d4$ISMSignalRatio,color=d8$SVMSig,size=d8$SVMSig))+
  geom_point(alpha=0.5)+
  geom_hline(yintercept = 0.06)+
  scale_color_manual(values=c("#e41a1c","#377eb8"),name="SVM Significant?")+
  scale_size_manual(values=c(0.1,1),name="SVM Significant")+
  ylab("regress signal ratio ISM")+
  xlab("SNP")+
  theme(legend.position = "bottom")

source('~/helpers.R')
multiplot(p1,p2,p3,p4,p5,p6,p7,p8,cols=4)

