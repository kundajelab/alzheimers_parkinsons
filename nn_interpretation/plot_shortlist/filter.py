import pandas as pd
data=open('ld_buddies_table_stage3.tsv','r').read().strip().split('\n')
outf=open('tmp','w')
outf.write(data[0]+'\n')
for line in data[1::]:
    tokens=line.split('\t')
    effect_allele=tokens[15]
    noneffect_allele=tokens[16]
    if effect_allele=="NA":
        continue
    if noneffect_allele=="NA":
        continue
    outf.write(line+'\n')

