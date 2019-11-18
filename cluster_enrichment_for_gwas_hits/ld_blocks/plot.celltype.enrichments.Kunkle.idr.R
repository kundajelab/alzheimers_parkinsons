rm(list=ls())
library(ggplot2)
cols=c("#FF0000",
            "#FFFF00",
            "#00EAFF",
            "#AA00FF",
            "#FF7F00",
            "#BFFF00",
            "#0095FF",
            "#FF00AA",
            "#FFD400",
            "#6AFF00",
            "#0040FF",
            "#EDB9B9",
            "#B9D7E9",
            "#E7E9B9",
            "#DCB9ED",
            "#B9EDE0",
            "#8F2323",
            "#23628F",
            "#8F6A23",
            "#6B238F",
            "#4F8F23",
            "#000000",
            "#737373",
            "#CCCCCC")

data=read.table("celltype.enrichments.Kunkle.idr.txt",header=TRUE,sep='\t')
ggplot(data=data,
       aes(x=data$Vcfbin,
           y=data$Fold,
           group=data$Cluster,
           color=data$Cluster))+
  geom_line(width=2)+
  scale_x_reverse()+
  scale_color_manual(name="Celltype",values=cols)+
  xlab("log p-value")+
  ylab("Fold Enrichment")+
  ggtitle("Kunkle 2019 GWAS enrichments, IDR Peaks")+
  theme_bw(20)
