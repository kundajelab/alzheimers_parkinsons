rm(list=ls())
library(ggplot2)
data=read.table("report.txt",header=TRUE,sep='\t')

p1=ggplot(data=data,
       aes(x=data$N_opt_overlap_reproducibility_qc))+
  geom_histogram(bins=10)+
  xlab("N Peaks")+
  ylab("N Bio Samples")+
  ggtitle("N_opt_overlap_reproducibility_qc")

p2=ggplot(data=data,
          aes(x=data$N_opt_idr_reproducibility_qc))+
  geom_histogram(bins=10)+
  xlab("N Peaks")+
  ylab("N Bio Samples")+
  ggtitle("N_opt_idr_reproducibility_qc")


p3=ggplot(data=data,
          aes(x=data$N_consv_overlap_reproducibility_qc))+
  geom_histogram(bins=10)+
  xlab("N Peaks")+
  ylab("N Bio Samples")+
  ggtitle("N_consv_overlap_reproducibility_qc")

p4=ggplot(data=data,
          aes(x=data$N_consv_idr_reproducibility_qc))+
  geom_histogram(bins=10)+
  xlab("N Peaks")+
  ylab("N Bio Samples")+
  ggtitle("N_consv_idr_reproducibility_qc")

p5=ggplot(data=data,
          aes(x=data$N1_overlap_reproducibility_qc))+
  geom_histogram(bins=10)+
  xlab("N Peaks")+
  ylab("N Bio Samples")+
  ggtitle("N1_overlap_reproducibility_qc")

p6=ggplot(data=data,
          aes(x=data$N1_idr_reproducibility_qc))+
  geom_histogram(bins=10)+
  xlab("N Peaks")+
  ylab("N Bio Samples")+
  ggtitle("N1_idr_reproducibility_qc")

