#generate html web page to visualize the SNP interpretations
import sys
from xml.etree import ElementTree as ET

#get the significant SNPs
snps=open('sigsnps.txt','r').read().strip().split('\n') 
clusters=list(range(1,25))
folds=list(range(0,10))


html=ET.Element('html')
head=ET.Element('head')
title=ET.Element('title')
title.text="ADPD Significant SNP NN Interpretation"
head.append(title) 
html.append(head)
body=ET.Element('body')
html.append(body)
maindiv=ET.Element('div')
body.append(maindiv)


#create table
table=ET.Element('table',attrib={'border':"1",'align':'center'})
maindiv.append(table)
#add top row
tr=ET.Element('tr')
table.append(tr)
td=ET.Element('td')
td.text='SNP'
tr.append(td)
for cluster in clusters:
    td=ET.Element('td')
    td.text='Cluster'+str(cluster)
    tr.append(td) 


for snp in snps:
    #add a row
    tr=ET.Element('tr')
    table.append(tr)
    td=ET.Element('td')
    td.text=snp
    tr.append(td)
    #iterate through the images
    for cluster in clusters:
        td=ET.Element('td')
        tr.append(td)
        image_html=str(cluster)+'/'+str(cluster)+'.'+snp+'.html'
        image_png=str(cluster)+'/'+str(0)+'/'+snp+'.'+str(cluster)+'.'+str(0)+'.png'
        a=ET.Element('a',attrib={'href':image_html})
        td.append(a)
        img=ET.Element('img',attrib={'src':image_png,'style':"height:3%;"})
        a.append(img)
        
        
        
ET.ElementTree(html).write('ADPD.sig.snps.nn.html',encoding='unicode',method='html')
