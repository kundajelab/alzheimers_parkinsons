import sys
import pandas as pd
import pdb 
forplot=pd.read_csv(sys.argv[1],header=0,sep='\t')
alleles=pd.read_csv(sys.argv[2],header=0,sep='\t')
forplot=forplot.merge(alleles,on='snp')
forplot.to_csv(sys.argv[3],index=False,sep='\t')

