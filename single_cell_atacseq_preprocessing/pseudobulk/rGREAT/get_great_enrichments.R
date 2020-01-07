rm(list=ls())
tasks=c("Cluster1.bed",
"Cluster2.bed",
"Cluster3.bed",
"Cluster4.bed",
"Cluster5.bed",
"Cluster6.bed",
"Cluster7.bed",
"Cluster8.bed",
"Cluster9.bed",
"Cluster10.bed",
"Cluster11.bed",
"Cluster12.bed",
"Cluster13.bed",
"Cluster14.bed",
"Cluster15.bed",
"Cluster16.bed",
"Cluster17.bed",
"Cluster18.bed",
"Cluster19.bed",
"Cluster20.bed",
"Cluster21.bed",
"Cluster22.bed",
"Cluster23.bed",
"Cluster24.bed")
#options(warn = -1)
#suppressWarnings(suppressPackageStartupMessages(library(rGREAT)))
library(rGREAT)
#args <- commandArgs(TRUE)
#fname=args[1]
#taskname=args[2]
## -------------------------------------------------------------------------------------------------
set.seed(123)
for(taskname in tasks){
fname=taskname
bed=read.table(fname,header=FALSE,sep='\t')
background=read.table('background.bed',header=FALSE,sep='\t')
eval=FALSE
curjob=submitGreatJob(bed,species="hg19",bg=background,request_interval = 10)
#wait
curjob
tb = getEnrichmentTables(curjob)
names(tb)
go_tables = getEnrichmentTables(curjob, category = c("GO"))
go_mol=go_tables[1]$`GO Molecular Function`
go_proc=go_tables[2]$`GO Biological Process`
go_cell=go_tables[3]$`GO Cellular Component`

#Apply filters on 
bh_thresh=0.05
lfc_thresh=1

go_mol=go_mol[go_mol$Hyper_Adjp_BH < bh_thresh,]
go_mol=go_mol[go_mol$Binom_Adjp_BH < bh_thresh,]
go_mol=go_mol[go_mol$Binom_Fold_Enrichment>lfc_thresh,] 


go_proc=go_proc[go_proc$Hyper_Adjp_BH<bh_thresh,]
go_proc=go_proc[go_proc$Binom_Adjp_BH<bh_thresh,]
go_proc=go_proc[go_proc$Binom_Fold_Enrichment>lfc_thresh,]

go_cell=go_cell[go_cell$Hyper_Adjp_BH<bh_thresh,]
go_cell=go_cell[go_cell$Binom_Adjp_BH<bh_thresh,]
go_cell=go_cell[go_cell$Binom_Fold_Enrichment>lfc_thresh,]


pathway_tables=getEnrichmentTables(curjob,category=c("Pathway Data"))
panther=pathway_tables[1]$`PANTHER Pathway`
biocyc=pathway_tables[2]$`BioCyc Pathway`
msigdb=pathway_tables[3]$`MSigDB Pathway`

panther=panther[panther$Hyper_Adjp_BH<bh_thresh,]
panther=panther[panther$Binom_Adjp_BH<bh_thresh,]
panther=panther[panther$Binom_Fold_Enrichment>lfc_thresh,]

biocyc=biocyc[biocyc$Hyper_Adjp_BH<bh_thresh,]
biocyc=biocyc[biocyc$Binom_Adjp_BH<bh_thresh,]
biocyc=biocyc[biocyc$Binom_Fold_Enrichment>lfc_thresh,]

msigdb=msigdb[msigdb$Hyper_Adjp_BH<bh_thresh,]
msigdb=msigdb[msigdb$Binom_Adjp_BH<bh_thresh,]
msigdb=msigdb[msigdb$Binom_Fold_Enrichment>lfc_thresh,]


#combine all results 
sig_results=rbind(panther,biocyc,msigdb,go_mol,go_proc,go_cell)
write.csv(sig_results,file=paste(taskname,'great',sep='.'),quote=TRUE,sep='\t')
}
