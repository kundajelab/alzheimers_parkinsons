merged_bim=open('merged.chr1.bim','r').read().strip().split('\n')
g1k_bim=open('1000g.Phase3.chr1.maf0.05.bim','r').read().strip().split('\n')
g1k_dict=dict()
seen=dict()
outf=open('1000g.Phase3.chr1.maf0.05.bim.recoded','w')
for line in g1k_bim:
    tokens=line.split()
    name=tokens[1]
    if name not in g1k_dict:        
        g1k_dict[name]=line
    outf.write(g1k_dict[name]+'\n')
outf.close() 
print('made dict')
outf=open('merged.chr1.bim.recoded','w')
for line in merged_bim:
    tokens=line.split()
    name=tokens[1]
    if name in g1k_dict:
        outf.write(g1k_dict[name]+'\n')
    else:
        if name not in seen:
            seen[name]=line            
            outf.write(line+'\n')
        else:
            outf.write(seen[name]+'\n')
        
outf.close()
