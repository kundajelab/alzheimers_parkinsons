rm(list=ls())
library(data.table)
library(ggplot2)
source("~/helpers.R")
#all 
caud=read.table("all_annotated/CAUD.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
caud$fract=caud$N_SUPPORTING_SAMPLES/caud$N_CANDIDATE_SAMPLES
p1=ggplot(data=caud,aes(x=caud$fract))+geom_histogram()+ggtitle("CAUD All")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

hipp=read.table("all_annotated/HIPP.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
hipp$fract=hipp$N_SUPPORTING_SAMPLES/hipp$N_CANDIDATE_SAMPLES
p2=ggplot(data=hipp,aes(x=hipp$fract))+geom_histogram()+ggtitle("HIPP All")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

mdfg=read.table("all_annotated/MDFG.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
mdfg$fract=mdfg$N_SUPPORTING_SAMPLES/mdfg$N_CANDIDATE_SAMPLES
p3=ggplot(data=mdfg,aes(x=mdfg$fract))+geom_histogram()+ggtitle("MDFG All")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

mdtg=read.table("all_annotated/MDTG.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
mdtg$fract=mdtg$N_SUPPORTING_SAMPLES/mdtg$N_CANDIDATE_SAMPLES
p4=ggplot(data=mdtg,aes(x=mdtg$fract))+geom_histogram()+ggtitle("MDTG All")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

parl=read.table("all_annotated/PARL.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
parl$fract=parl$N_SUPPORTING_SAMPLES/parl$N_CANDIDATE_SAMPLES
p5=ggplot(data=parl,aes(x=parl$fract))+geom_histogram()+ggtitle("PARL All")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

ptmn=read.table("all_annotated/PTMN.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
ptmn$fract=ptmn$N_SUPPORTING_SAMPLES/ptmn$N_CANDIDATE_SAMPLES
p6=ggplot(data=ptmn,aes(x=ptmn$fract))+geom_histogram()+ggtitle("PTMN All")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

smtg=read.table("all_annotated/SMTG.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
smtg$fract=smtg$N_SUPPORTING_SAMPLES/smtg$N_CANDIDATE_SAMPLES
p7=ggplot(data=smtg,aes(x=smtg$fract))+geom_histogram()+ggtitle("SMTG All")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

suni=read.table("all_annotated/SUNI.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
suni$fract=suni$N_SUPPORTING_SAMPLES/suni$N_CANDIDATE_SAMPLES
p8=ggplot(data=suni,aes(x=suni$fract))+geom_histogram()+ggtitle("SUNI All")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

#controls
cont_caud=read.table("controls_annotated/CAUD.ctr.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
cont_caud$fract=cont_caud$N_SUPPORTING_SAMPLES/cont_caud$N_CANDIDATE_SAMPLES
p9=ggplot(data=cont_caud,aes(x=cont_caud$fract))+geom_histogram()+ggtitle("CAUD Controls")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

cont_hipp=read.table("controls_annotated/HIPP.ctr.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
cont_hipp$fract=cont_hipp$N_SUPPORTING_SAMPLES/cont_hipp$N_CANDIDATE_SAMPLES
p10=ggplot(data=cont_hipp,aes(x=cont_hipp$fract))+geom_histogram()+ggtitle("HIPP Controls")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

cont_mdfg=read.table("controls_annotated/MDFG.ctr.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
cont_mdfg$fract=cont_mdfg$N_SUPPORTING_SAMPLES/cont_mdfg$N_CANDIDATE_SAMPLES
p11=ggplot(data=cont_mdfg,aes(x=cont_mdfg$fract))+geom_histogram()+ggtitle("MDFG Controls")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

cont_mdtg=read.table("controls_annotated/MDTG.ctr.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
cont_mdtg$fract=cont_mdtg$N_SUPPORTING_SAMPLES/cont_mdtg$N_CANDIDATE_SAMPLES
p12=ggplot(data=cont_mdtg,aes(x=cont_mdtg$fract))+geom_histogram()+ggtitle("MDTG Controls")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

cont_parl=read.table("controls_annotated/PARL.ctr.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
cont_parl$fract=cont_parl$N_SUPPORTING_SAMPLES/cont_parl$N_CANDIDATE_SAMPLES
p13=ggplot(data=cont_parl,aes(x=cont_parl$fract))+geom_histogram()+ggtitle("PARL Controls")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

cont_ptmn=read.table("controls_annotated/PTMN.ctr.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
cont_ptmn$fract=cont_ptmn$N_SUPPORTING_SAMPLES/cont_ptmn$N_CANDIDATE_SAMPLES
p14=ggplot(data=cont_ptmn,aes(x=cont_ptmn$fract))+geom_histogram()+ggtitle("PTMN Controls")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

cont_smtg=read.table("controls_annotated/SMTG.ctr.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
cont_smtg$fract=cont_smtg$N_SUPPORTING_SAMPLES/cont_smtg$N_CANDIDATE_SAMPLES
p15=ggplot(data=cont_smtg,aes(x=cont_smtg$fract))+geom_histogram()+ggtitle("SMTG Controls")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

cont_suni=read.table("controls_annotated/SUNI.ctr.optimal.idr.narrowPeak.annotated.txt",header=TRUE,sep='\t')
cont_suni$fract=cont_suni$N_SUPPORTING_SAMPLES/cont_suni$N_CANDIDATE_SAMPLES
p16=ggplot(data=cont_suni,aes(x=cont_suni$fract))+geom_histogram()+ggtitle("SUNI Controls")+xlab("Fract. Samples with Peak")+ylab("N peaks")+geom_vline(xintercept=0.3)+theme_bw()

svg("reproducibility_fraction_across_samples_by_region_idr.svg",height=11,width=6,pointsize=12)
print(multiplot(p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,cols=2))
dev.off()


