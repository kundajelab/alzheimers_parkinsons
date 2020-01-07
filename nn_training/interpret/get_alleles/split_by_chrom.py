data=open("no_alleles_chrom_rs.csv",'r').read().strip().split('\n')
chrom_dict=dict()
for line in data:
    tokens=line.split('\t')
    chrom=tokens[0]
    if chrom not in chrom_dict:
        chrom_dict[chrom]=[] 
    snp=tokens[1]
    if snp.startswith('rs')==False:
        snp=int(snp.split('_')[1])
    chrom_dict[chrom].append(snp)
for chrom in chrom_dict:
    outf=open(chrom+".snps",'w')
    for snp in chrom_dict[chrom]:
        outf.write(str(snp)+'\n')
        
        
