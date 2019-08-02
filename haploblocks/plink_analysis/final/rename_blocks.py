blocks=open("plink.blocks",'r').read().strip().split('\n') 
outf=open("plink.blocks.names_resolved",'w')
name_conversions=open("name_resolutions.txt",'r').read().strip().split('\n') 
conversion_dict=dict() 
for row in name_conversions: 
    tokens=row.split(':') 
    conversion_dict[tokens[0]]=tokens[1] 
for row in blocks: 
    tokens=row.split() 
    outline=[] 
    for token in tokens: 
        if token not in conversion_dict: 
            outline.append(token) 
        else: 
            outline.append(conversion_dict[token]) 
    outf.write(' '.join(outline)+'\n')

