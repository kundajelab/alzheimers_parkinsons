import pandas as pd
block_to_pval=dict()
for i in range(-10,0):
    intersection=open("blocks.Kunkle.overlap."+str(i)+".bed",'r').read().strip().split('\n')
    for line in intersection:
        if line not in block_to_pval:
            block_to_pval[line]=[i]
        else:
            block_to_pval[line].append(i)
#got map of blocks to GWAS pvalue
for block in block_to_pval:
    block_to_pval[block]=min(block_to_pval[block])
all_blocks=open("fourier_ls-all.bed",'r').read().strip().split('\n')
for i in range(-10,0):
    outf=open("Kunkle.blocks."+str(i)+".bed",'w')
    for block in all_blocks:
        if block not in block_to_pval:
            continue
        if block_to_pval[block]<=i:
            outf.write(block+'\n')
    outf.close()
    
    
block_to_pval=dict()
for i in range(-10,0):
    intersection=open("blocks.23andme.overlap."+str(i)+".bed",'r').read().strip().split('\n')
    for line in intersection:
        if line not in block_to_pval:
            block_to_pval[line]=[i]
        else:
            block_to_pval[line].append(i)
#got map of blocks to GWAS pvalue
for block in block_to_pval:
    block_to_pval[block]=min(block_to_pval[block])
all_blocks=open("fourier_ls-all.bed",'r').read().strip().split('\n')
for i in range(-10,0):
    outf=open("23andme.blocks."+str(i)+".bed",'w')
    for block in all_blocks:
        if block not in block_to_pval:
            continue
        if block_to_pval[block]<=i:
            outf.write(block+'\n')
    outf.close()
    
