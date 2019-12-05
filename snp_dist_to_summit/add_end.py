data=open('tmp2','r').read().strip().split('\n')
outf=open('tmp3','w')
for line in data:
    tokens=line.split('\t')
    outf.write(tokens[0]+'\t'+tokens[1]+'\t'+str(int(tokens[1])+1)+'\t'+tokens[2]+'\n')
    
