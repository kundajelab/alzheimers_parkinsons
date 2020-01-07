blocks=open("plink.blocks.det",'r').read().strip().split('\n') 
outf=open("plink.blocks.det.names_resolved",'w')
name_conversions=open("name_resolutions.txt",'r').read().strip().split('\n') 
conversion_dict=dict() 
for row in name_conversions: 
    tokens=row.split(':') 
    conversion_dict[tokens[0]]=tokens[1] 
for row in blocks: 
    tokens=row.split() 
    print(tokens)
    outline=tokens[0:5] 
    snps=[] 
    for token in tokens[5].split('|'): 
        if token not in conversion_dict: 
            snps.append(token) 
        else: 
            snps.append(conversion_dict[token]) 
    snps='|'.join(snps) 
    outline.append(snps) 
    outf.write('\t'.join(outline)+'\n')

