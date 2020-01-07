library(GenomicRanges)
library(BiocGenerics)
library(parallel)
args = commandArgs(trailingOnly=TRUE)
input_rds=args[1]
outf=args[2]
print(paste(input_rds,'->',outf))
#read in the RDS data frame
rds_data=readRDS(input_rds)
frag_len=as.data.frame(table(end(rds_data)-start(rds_data)))
gz_file=gzfile(outf,'w')
print("opened output file")
write.table(frag_len,gz_file,row.names=FALSE,col.names=TRUE,sep='\t',quote=FALSE)
close(gz_file)
print("done!")