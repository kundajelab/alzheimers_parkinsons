#7/24/19

#Read in fragment files and convert to bed files
#Run on Sherlock
library(ArchRx)
frag_dir <- "/oak/stanford/groups/howchang/users/mcorces/Brain_All/analysis/scATAC/Cluster_Analyses/fragments/"
frag_files <- list.files(frag_dir, pattern = "fragments.rds$", full.names = TRUE)
for (x in frag_files) {
  print(paste0("Processing ",x))
  gr <- readRDS(x)
  cluster <- gsub(x = basename(x), pattern = "-fragments.rds", replacement = "")
  dir.create(paste0(frag_dir,"/peakCalls/"))
  callMacs2(fragments = gr, directory = paste0(frag_dir,"/peakCalls/"), sample_name = cluster, genome_size = 2.7E9, shift = -75, extsize = 150, cutoff = 0.01, method = "q", getInsertions = TRUE, read_summits = FALSE, remove = TRUE)
}


#Threshold narrowPeak files
spm <- 2 #score per million cutoff

peak_dir <- "K:/Shared drives/Brain_Merged/Analysis/scATAC/190713/Cluster_Analyses/peakCalls/"
peak_files <- list.files(peak_dir, pattern = "_peaks.narrowPeak$", full.names = TRUE)

# extraCols_narrowPeak <- c(signalValue = "numeric", pValue = "numeric",
#                           qValue = "numeric", peak = "integer")
# 
# gr <- import(peak_files[1], format = "BED", extraCols = extraCols_narrowPeak)
# gr <- gr[order(gr$score, decreasing = TRUE)]
# 
# ggPlotPoint(x = seq(from = 1, to = length(gr), by = 1), y = (gr$score / (sum(gr$score)/1000000))) + geom_hline(yintercept = 5)

for (x in peak_files) {
  peaks <- read.table(x, header = FALSE, sep = "\t", row.names = NULL)
  peaks$spm <- peaks[,5]/(sum(peaks[,5])/1000000)
  peaks <- peaks[order(peaks$spm, decreasing = TRUE),]
  num <- length(which(peaks$spm >= spm))
  print(paste0(num," peaks above spm = ", spm, " in file ",basename(x)))
  colnames(peaks) <- c("chr","start","stop","peakID","MACS2_score","blank","MACS2_foldChange","MACS2_negLog10pvalue","MACS2_negLog10qvalue","MACS2_summitPosition","ScorePerMillion")
  write.table(peaks[which(peaks$ScorePerMillion >= spm),],
              file = gsub(x = x, pattern = "_peaks.narrowPeak", replacement = paste0("_peaks.narrowPeak_TrimmedSPM",spm,".txt")),
              quote = FALSE, sep = "\t", col.names = TRUE, row.names = FALSE)
}

