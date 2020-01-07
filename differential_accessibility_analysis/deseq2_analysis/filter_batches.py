data=open('batches.txt','r').read().strip().split('\n')
outf=open('batches.filtered.csv','w')
tech_rep_dict=dict()
outf.write(data[0]+'\n')
for line in data[1::]:
    tokens=line.split('\t')
    sample_id=tokens[0]
    sample_id=sample_id.split('X')[0].rstrip('_')
    if sample_id.startswith('PD'):
        sample_id=sample_id[3::].split('_')
        base=sample_id[2::]
        base.append(sample_id[0])
        base.append(sample_id[1])
        sample_id='_'.join(base) 
    print(sample_id) 
    if sample_id not in tech_rep_dict:
        tech_rep_dict[sample_id]=line
for key in tech_rep_dict:
    outf.write(key+'\t'+tech_rep_dict[key]+'\n')
    
