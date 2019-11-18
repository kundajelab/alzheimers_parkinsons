rm(list=ls())
library(rGREAT)
set.seed(123)
for(task in seq(1,24)){
ftask=paste("Cluster",task,".bed",sep="")
fbackground=paste("background.Cluster",task,".bed",sep="")
bed=read.table(ftask,header=FALSE,sep='\t')
background=read.table(fbackground,header=FALSE,sep='\t')
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
bh_thresh=0.2
lfc_thresh=1

go_mol=go_mol[go_mol$Hyper_Adjp_BH < bh_thresh,]
go_proc=go_proc[go_proc$Hyper_Adjp_BH<bh_thresh,]
go_cell=go_cell[go_cell$Hyper_Adjp_BH<bh_thresh,]

pathway_tables=getEnrichmentTables(curjob,category=c("Pathway Data"))
panther=pathway_tables[1]$`PANTHER Pathway`
biocyc=pathway_tables[2]$`BioCyc Pathway`
msigdb=pathway_tables[3]$`MSigDB Pathway`

panther=panther[panther$Hyper_Adjp_BH<bh_thresh,]

biocyc=biocyc[biocyc$Hyper_Adjp_BH<bh_thresh,]

msigdb=msigdb[msigdb$Hyper_Adjp_BH<bh_thresh,]


#combine all results 
sig_results=rbind(panther,biocyc,msigdb,go_mol,go_proc,go_cell)
print(head(sig_results))
write.csv(sig_results,file=paste(task,'great',sep='.'),quote=TRUE,sep='\t')
}
