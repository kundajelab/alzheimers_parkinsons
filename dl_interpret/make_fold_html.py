#generate html web page to visualize the SNP interpretations
import sys
from xml.etree import ElementTree as ET

#get the significant SNPs
snps=open('sigsnps.txt','r').read().strip().split('\n') 
clusters=list(range(1,25))
folds=list(range(0,10))

for snp in snps:
    for cluster in clusters: 
        html=ET.Element('html')
        head=ET.Element('head')
        title=ET.Element('title')
        title.text=snp+":"+str(cluster) 
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
        for fold in folds:
            td=ET.Element('td')
            td.text='Fold'+str(fold)
            tr.append(td) 
        image_tr=ET.Element('tr')
        table.append(image_tr)
        placeholder_td=ET.Element('td')
        placeholder_td.text=snp
        image_tr.append(placeholder_td)
        for fold in folds:
            image_td=ET.Element('td')
            image_tr.append(image_td)
            image_png=str(fold)+'/'+snp+'.'+str(cluster)+'.'+str(fold)+'.png'
            img=ET.Element('img',attrib={'src':image_png,'style':"height:40%;"})
            image_td.append(img)
        ET.ElementTree(html).write(str(cluster)+'.'+str(snp)+'.html',encoding='unicode',method='html')
