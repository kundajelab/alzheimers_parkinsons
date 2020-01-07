rows_to_pull=open('rows_to_pull','r').read().strip().split('\n') 
row_dict=dict() 
for row in rows_to_pull: 
    row_dict[int(row)]=1 
dataf=open("1000GP_Phase3/1000GP_Phase3_chr17.hap",'r')
outf=open("haplotypes_tokeep.txt",'w')
cur_row=0
for line in dataf: 
    if cur_row in row_dict:
        outf.write(line) 
        print("wrote!")
    cur_row+=1 
    if cur_row % 100000==0: 
        print(cur_row) 

