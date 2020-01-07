rm(list=ls())
library(gplots)
require(gtools)
require(RColorBrewer)
files=c("sig.snps.classification.GradSignalRatio",
        "sig.snps.classification.GradTotalSignal",
        "sig.snps.classification.ISMSignalRatio",
        "sig.snps.classification.ISMTotalSignal",
        "sig.snps.regression.GradSignalRatio",
        "sig.snps.regression.GradTotalSignal",
        "sig.snps.regression.ISMSignalRatio",
        "sig.snps.regression.ISMTotalSignal")
for (filename in files){
#data=read.table("sig.snps.metric.tally.txt",header=TRUE,sep='\t', row.names = 1)
data=read.table(paste(filename,"txt",sep='.'),header=TRUE,sep='\t', row.names = 1)
data=as.matrix(data)
data=t(data)
cols <- colorRampPalette(brewer.pal(10, "RdBu"))(256)
svg(paste(filename,"svg",sep='.'),height = 8,width=20, pointsize=12)
cur_h=heatmap.2(data,
                col=rev(cols),
                trace="none",
                scale="none",
                Rowv=FALSE,
                Colv=TRUE,
                dendrogram="none",
                main=paste(filename,"n=123 SVM-sig SNPs",sep = " "),
                symbreak=FALSE)
dev.off() 
}
