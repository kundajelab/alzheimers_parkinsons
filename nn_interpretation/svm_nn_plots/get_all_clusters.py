data=open('tmp','r').read().strip().split('\n')
outf=open('nn_sig_from123.txt','w')
for line in data:
    tokens=line.split('\t')
    snp=tokens[0]
    fold=tokens[1]
    for cluster in range(1,25):
        outf.write(snp+'\t'+str(cluster)+'\t'+fold+'\n')
        
