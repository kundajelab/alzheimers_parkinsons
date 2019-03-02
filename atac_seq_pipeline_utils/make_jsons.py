import sys
import os
import json
import pandas as pd

def main(args):

    sep = os.path.sep
    adpd = '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/'
    cohort = 'AD'
    techreps = {}
    metadata = pd.read_excel(adpd + '190215_Brain-All_Metadata_Merged.xlsx')
    os.mkdir(adpd + cohort)
    types = ['ADAD','CTRH','CTRL','LOAD']
    regions = ['CAUD','HIPP','PARL','SMTG']
    for x in types:
        os.mkdir(adpd + cohort + sep + x)
        for y in regions:
            os.mkdir(adpd + cohort + sep + x + sep + y)
    for index, row in metadata.iterrows():
        if row['Cohort'] == cohort:
            if '_'.join([row['Type'], row['Region'], row['PatientID']]) in techreps:
                techreps['_'.join([row['Type'], row['Region'], row['PatientID']])].append(row['Bam'])
            else:
                techreps['_'.join([row['Type'], row['Region'], row['PatientID']])] = [row['Bam']]
    for i in techreps:
        keysplit = i.split('_')
        with open(adpd + cohort + sep + keysplit[0] + sep + keysplit[1] + sep + i + '.json', 'w') as outfile:
            outfile.write('{\n')
            outfile.write('\t"atac.pipeline_type": "atac",\n')
            outfile.write('\t"atac.genome_tsv": "/home/groups/cherry/encode/pipeline_genome_data/hg38_sherlock.tsv",\n')
            outfile.write('\t"atac.bams": ' + json.dumps(techreps[i]) + ',\n')
            outfile.write('\t"atac.paired_end": true,\n')
            outfile.write('\t"atac.enable_idr": true,\n')
            outfile.write('\t"atac.idr_thresh": 0.05\n')
            outfile.write('}')


if __name__ == "__main__":
    main(sys.argv[1:])
