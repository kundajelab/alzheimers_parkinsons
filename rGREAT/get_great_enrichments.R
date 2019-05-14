rm(list=ls())
#run on sva-corrected limma samples 
fnames_full=c("../lift_hg38_hg19/hg19.expanded_sva_diff_ad_caud_adad_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_caud_adad_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_caud_adad_vs_load.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_caud_ctrl_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_caud_load_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_caud_load_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_hipp_adad_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_hipp_adad_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_hipp_adad_vs_load.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_hipp_ctrl_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_hipp_load_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_hipp_load_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_parl_adad_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_parl_adad_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_parl_adad_vs_load.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_parl_ctrl_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_parl_load_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_parl_load_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_smtg_adad_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_smtg_adad_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_smtg_adad_vs_load.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_smtg_ctrl_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_smtg_load_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_smtg_load_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_caud_gba1_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_caud_gba1_vs_lrrk.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_caud_gba1_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_caud_lrrk_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_caud_lrrk_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_caud_spor_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_hipp_gba1_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_hipp_gba1_vs_lrrk.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_hipp_gba1_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_hipp_lrrk_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_hipp_lrrk_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_hipp_spor_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdfg_gba1_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdfg_gba1_vs_lrrk.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdfg_gba1_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdfg_lrrk_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdfg_lrrk_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdfg_spor_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdtg_gba1_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdtg_gba1_vs_lrrk.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdtg_gba1_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdtg_lrrk_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdtg_lrrk_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdtg_spor_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_ptmn_gba1_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_ptmn_gba1_vs_lrrk.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_ptmn_gba1_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_ptmn_lrrk_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_ptmn_lrrk_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_ptmn_spor_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_suni_gba1_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_suni_gba1_vs_lrrk.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_suni_gba1_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_suni_lrrk_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_suni_lrrk_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_suni_spor_vs_ctrl.tsv.bed")
fnames=c(
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_hipp_load_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_hipp_load_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_parl_adad_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_parl_adad_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_parl_adad_vs_load.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_parl_load_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_smtg_adad_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_smtg_adad_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_smtg_adad_vs_load.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_ad_smtg_load_vs_ctrh.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_caud_gba1_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_caud_gba1_vs_lrrk.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_caud_lrrk_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_caud_lrrk_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_caud_spor_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_hipp_gba1_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_hipp_gba1_vs_lrrk.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_hipp_gba1_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_hipp_lrrk_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_hipp_lrrk_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_hipp_spor_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdfg_gba1_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdfg_gba1_vs_lrrk.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdfg_lrrk_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdfg_lrrk_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdfg_spor_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdtg_gba1_vs_lrrk.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdtg_lrrk_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_mdtg_lrrk_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_ptmn_gba1_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_ptmn_gba1_vs_lrrk.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_ptmn_gba1_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_ptmn_lrrk_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_ptmn_lrrk_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_suni_gba1_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_suni_gba1_vs_lrrk.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_suni_gba1_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_suni_lrrk_vs_ctrl.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_suni_lrrk_vs_spor.tsv.bed",
"../lift_hg38_hg19/hg19.expanded_sva_diff_pd_suni_spor_vs_ctrl.tsv.bed")
options(warn = -1)
suppressWarnings(suppressPackageStartupMessages(library(rGREAT)))
library(rGREAT,quietly=TRUE)
#args <- commandArgs(TRUE)
#fname=args[1]

## -------------------------------------------------------------------------------------------------
set.seed(123)
for(fname in fnames){
bed = read.table(fname,header=FALSE,sep='\t')
job = submitGreatJob(bed, species="hg19",request_interval = 20)
#browser()  #necessary to avoid the job query timing out. Also from rstudio use ctl+shift+enter to execute with echo.
#Sys.sleep(10)
tb = getEnrichmentTables(job)
names(tb)
go_tables = getEnrichmentTables(job, category = c("GO"))
go_mol=go_tables[1]$`GO Molecular Function`
go_proc=go_tables[2]$`GO Biological Process`
go_cell=go_tables[3]$`GO Cellular Component`

#Apply filters on 

go_mol=go_mol[go_mol$Hyper_Adjp_BH < 0.05,]
go_mol=go_mol[go_mol$Binom_Adjp_BH < 0.05,]
go_mol=go_mol[go_mol$Binom_Fold_Enrichment>1,] 


go_proc=go_proc[go_proc$Hyper_Adjp_BH<0.05,]
go_proc=go_proc[go_proc$Binom_Adjp_BH<0.05,]
go_proc=go_proc[go_proc$Binom_Fold_Enrichment>1,]

go_cell=go_cell[go_cell$Hyper_Adjp_BH<0.05,]
go_cell=go_cell[go_cell$Binom_Adjp_BH<0.05,]
go_cell=go_cell[go_cell$Binom_Fold_Enrichment>1,]


pathway_tables=getEnrichmentTables(job,category=c("Pathway Data"))
panther=pathway_tables[1]$`PANTHER Pathway`
biocyc=pathway_tables[2]$`BioCyc Pathway`
msigdb=pathway_tables[3]$`MSigDB Pathway`

panther=panther[panther$Hyper_Adjp_BH<0.05,]
panther=panther[panther$Binom_Adjp_BH<0.05,]
panther=panther[panther$Binom_Fold_Enrichment>1,]

biocyc=biocyc[biocyc$Hyper_Adjp_BH<0.05,]
biocyc=biocyc[biocyc$Binom_Adjp_BH<0.05,]
biocyc=biocyc[biocyc$Binom_Fold_Enrichment>1,]

msigdb=msigdb[msigdb$Hyper_Adjp_BH<0.05,]
msigdb=msigdb[msigdb$Binom_Adjp_BH<0.05,]
msigdb=msigdb[msigdb$Binom_Fold_Enrichment>1,]


#combine all results 
sig_results=rbind(panther,biocyc,msigdb,go_mol,go_proc,go_cell)
write.csv(sig_results,file=paste(fname,'great',sep='.'),quote=TRUE,sep='\t')
}
