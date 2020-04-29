adpd=open('merged.chr1.bim','r').read().strip().split('\n')
g1k=open('1000g.Phase3.chr1.maf0.05.bim','r').read().strip().split('\n')
adpd_dict=dict() 
adpd_set=set([])
g1k_set=set([])
print("loaded data")
for line in adpd:
    tokens=line.split()
    name=tokens[1]
    adpd_set.add(name)
    adpd_dict[name]=line 
print("made adpd dict") 
for line in g1k:
    tokens=line.split()
    name=tokens[1]
    g1k_set.add(name)
print("made 1000g dict")
common=adpd_set.intersection(g1k_set)
print("got intersection")
print(len(common))
common=list(common)
outf=open('shared.snps.txt','w')
for entry in common:
    cur_line=adpd_dict[entry]
    outf.write(cur_line+'\n') 
outf.close()
