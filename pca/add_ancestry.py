data=open("/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/individual_bams/pca/adpd.1kg.merged.common.pca.eigenvec",'r').read().strip().split('\n')
ancestry=[i.split() for i in open("/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/individual_bams/pca/20130606_sample_info.csv",'r').read().strip().split('\n')]
ancestry_dict=dict()
for line in ancestry[1::]:
    ancestry_dict[line[0]]=line[1]
super_pop=open('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/individual_bams/pca/super_pop.txt','r').read().strip().split('\n')
super_pop_dict=dict()
for line in super_pop[1::]:
    tokens=line.split('\t')
    pop=tokens[0]
    superpop=tokens[2]
    super_pop_dict[pop]=superpop
    
outf=open('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mpileup/individual_bams/pca/adpd.1kg.merged.common.pca.eigenvec.with.ancestry','w')
header=data[0]+'\tAncestry\tGeoRegion'
outf.write(header+'\n')
for line in data[1::]:
    tokens=line.split('\t')
    iid=tokens[3]
    if iid in ancestry_dict:
        cur_ancestry=ancestry_dict[iid]
        cur_region=super_pop_dict[cur_ancestry]
        outf.write(line+'\t'+cur_ancestry+'\t'+cur_region+'\n')
    else:
        outf.write(line+'\tADPD\tADPD\n')
outf.close()
