import pandas as pd
bim=pd.read_csv("chr17_phase3_bed_range.bim",header=None,sep='\t')
coords=pd.read_csv("../../hg19_coords.csv",header=None,sep='\t') 
coord_dict=dict() 
for index,row in coords.iterrows(): 
    coord=row[1] 
    name=row[3] 
    coord_dict[coord]=name 
print("made coord dict") 
for index,row in bim.iterrows(): 
    coord=row[3] 
    name=row[1] 
    if coord in coord_dict: 
        proper_name=coord_dict[coord] 
        if name!=proper_name: 
            print(name+":"+proper_name)
