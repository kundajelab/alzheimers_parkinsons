import pandas as pd
import os
from splits import *
import pysam

splits = range(10)

basedir = '/mnt/lab_data3/soumyak/adpd/gkmsvm/'
ref_fasta = '/mnt/lab_data3/soumyak/refs/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta'
ref = pysam.FastaFile(ref_fasta)

clusters = [cluster for cluster in os.listdir(basedir)]
for cluster in clusters:
    print(cluster)
    data = pd.read_csv(basedir+str(cluster)+'/peaks/all_idr_peaks.bed', header=None, sep='\t')
    new_data = data.copy()
    for index,row in data.iterrows():
        scores = [float(x) for x in row[3].split(',')]
        summits = [int(x) for x in row[4].split(',')]
        max_score_index = scores.index(max(scores))
        new_data.at[index, 3] = scores[max_score_index]
        new_data.at[index, 4] = summits[max_score_index]
    new_data.sort_values(by=3, ascending=False, inplace=True)
    new_data.to_csv(basedir+str(cluster)+'/peaks/idr_peaks.bed', header=False, index=False, sep='\t')
    data = pd.read_csv(basedir+str(cluster)+'/peaks/idr_peaks.bed', header=None, sep='\t')
    for split in splits:
        print("Fold: ", split)
        train_bed = open(basedir+str(cluster)+'/fold'+str(split)+'/train/train.pos.bed', 'w')
        test_bed = open(basedir+str(cluster)+'/fold'+str(split)+'/test/test.pos.bed', 'w')
        train_fasta = open(basedir+str(cluster)+'/fold'+str(split)+'/train/train.pos.fasta', 'w')
        test_fasta = open(basedir+str(cluster)+'/fold'+str(split)+'/test/test.pos.fasta', 'w')
        train_counter = 0
        test_counter = 0
        for index,row in data.iterrows():
            chrom = str(row[0])
            if 'chr' not in chrom:
                chrom = 'chr' + chrom
            test_chroms = hg19_splits[split]['test']
            summit = int(row[4])
            start = int(row[1]) + summit - 500
            end = start + 1000
            seq = ref.fetch(chrom,start,end)
            seq = seq.upper()
            if 'N' in seq:
                continue
            if chrom in test_chroms:
                test_bed.write('\t'.join([chrom, str(start), str(end), str(row[3]), str(row[4])])+'\n')
                test_fasta.write('>' + str(test_counter) + '\n')
                test_fasta.write(seq + '\n')
                test_counter += 1
            else:
                if train_counter < 60000:
                    train_bed.write('\t'.join([chrom, str(start), str(end), str(row[3]), str(row[4])])+'\n')
                    train_fasta.write('>' + str(train_counter) + '\n')
                    train_fasta.write(seq + '\n')
                    train_counter += 1
