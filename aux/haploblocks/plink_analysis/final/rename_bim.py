bim=open("chr17_phase3_bed_range.bim",'r').read().strip().split('\n') 
outf=open("chr17_phase3_bed_range.bim.names_resolved",'w')
name_conversions=open("name_resolutions.txt",'r').read().strip().split('\n') 
conversion_dict=dict() 
for row in name_conversions: 
    tokens=row.split(':') 
    conversion_dict[tokens[0]]=tokens[1] 
for row in bim: 
    tokens=row.split() 
    if tokens[1] in conversion_dict: 
        tokens[1]=conversion_dict[tokens[1]]
    outf.write('\t'.join(tokens)+'\n')

