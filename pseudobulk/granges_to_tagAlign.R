#!/usr/bin/env Rscript
##converts a GRanges object to a stranded tagAlign file
#get the dependencies
library(GenomicRanges)
library(BiocGenerics)
library(parallel)



args = commandArgs(trailingOnly=TRUE)
input_rds=args[1]
output_tagAlign=args[2]
seqlen=as.integer(args[3])

print(paste(input_rds,'->',output_tagAlign))
#read in the RDS data frame
rds_data=readRDS(input_rds)
print("loaded RDS df")
browser() 
#rds_data
chroms=seqnames(rds_data)
#get positive strands
pos_start=start(rds_data)-1
pos_end=pos_start+seqlen
pos_df=data.frame(chroms,pos_start,pos_end)
pos_df$sequence="N"
pos_df$score=1000
pos_df$strand="+"
print("got positive strand data frame") 
#get negative strands
neg_end=end(rds_data)-1
neg_start=neg_end-seqlen
neg_df=data.frame(chroms,neg_start,neg_end)
neg_df$sequence="N"
neg_df$score=1000
neg_df$strand="-"
print("got negative strand data frame")

rm(rds_data)
print("deleted rds object") 
#concatenate the positive and negative data frames
names(pos_df)=c('chrom','start','end','seq','score','strand')
names(neg_df)=c('chrom','start','end','seq','score','strand')
df=rbind(pos_df,neg_df) 
print("concatenated positive and negative strands") 
#save to tagAlign, gzipped
gz_file=gzfile(output_tagAlign,'w')
print("opened output file")
write.table(df,gz_file,row.names=FALSE,col.names=FALSE,sep='\t',quote=FALSE)
close(gz_file)
print("done!")