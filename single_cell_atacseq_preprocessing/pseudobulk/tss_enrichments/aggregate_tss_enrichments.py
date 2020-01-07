#aggregate tss enrichments across clusters
base_dir="/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_tss/Cluster"
outf=open('tss_enrichments.txt','w')
outf.write('Cluster\tEnrichment\n')
for cluster in range(1,25):
    tss_enrichment=open(base_dir+str(cluster)+"/"+"Cluster"+str(cluster)+".sorted.tss_enrich.qc",'r').read().strip()
    outf.write(str(cluster)+'\t'+str(tss_enrichment)+'\n')
