from kerasAC.chrom_to_split import *
data=open('nn_unique.txt','r').read().strip().split('\n')
outf=open('nn_unique_annotated.txt','w')
outf.write('snp\tcluster\tfold\teffect\tnoneffect\n')
for line in data:
    tokens=line.split('\t')
    chrom=tokens[0]
    fold=hg38_chrom_to_split[chrom]
    rsid=tokens[1]
    effect=tokens[2]
    noneffect=tokens[3]
    for cluster in range(1,25):
        outf.write(rsid+'\t'+str(cluster)+'\t'+str(fold)+'\t'+str(effect)+'\t'+str(noneffect)+'\n')
        
