import os
import pysam
import pickle
import random
import pybedtools
import numpy as np
import tabix as tb
import pandas as pd
from kerasAC.splits import *

np.random.seed(1234)


ref_fasta = '/mnt/data/pipeline_genome_data/hg19/male.hg19.fa'
ref_gen = pysam.FastaFile(ref_fasta)


dbsnp = tb.open('/mnt/lab_data3/soumyak/refs/hg19/dbSNP/00-All.vcf.gz')
for cluster in range(1,25):
    print(cluster)
    ld_snps = '/mnt/lab_data2/annashch/alzheimers_parkinsons/cluster_enrichment_for_gwas_hits/intersections/intersection.Kunkle.idr.clusters.Cluster'+str(cluster)+'.idr.optimal.narrowPeak'
    ld = pd.read_csv(ld_snps, header=None, sep='\t')
    ld = ld[[3, 4, 5, 6]]
    ld.rename(columns={3:'chrom', 4:'start', 5:'end', 6:'rsid'}, inplace=True)
    for fold in range(10):
        print("Fold: ", fold)
        basedir = '/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+str(cluster)+'/fold'+str(fold)+'/test/'
        gwas_bed = open(basedir + 'gwas.pos.bed', 'w')
        ref_fasta = open(basedir + 'ref.pos.fasta', 'w')
        alt_fasta = open(basedir + 'alt.pos.fasta', 'w')
        counter = 0
        for index,row in ld.iterrows():
            chrom = row['chrom']
            if chrom in hg19_splits[fold]['test']:
                snp_start = int(row['start'])
                snp_end = int(row['end'])
                rsid = row['rsid']
                matches = dbsnp.query(chrom.strip('chr'), snp_start, snp_end)
                gotmatches = False
                for match in matches:
                    if match[2] == rsid:
                        ref = match[3]
                        alts = match[4].split(',')
                        gotmatches = True
                        break
                if gotmatches:
                    start = snp_end - 500
                    end = snp_end + 500
                    seq = ref_gen.fetch(chrom, start, end)
                    seq = seq.upper()
                    if 'N' in seq:
                        continue
                    left = seq[0:500]
                    ref_right = seq[500+len(ref):]
                    ref_seq = left + ref + ref_right
                    assert len(ref_seq) == 1000
                    for alt in alts:
                        alt_right = seq[500+len(alt):]
                        alt_seq = left + alt + alt_right
                        assert len(alt_seq) == 1000
                        gwas_bed.write('\t'.join([chrom, str(snp_start), str(snp_end), rsid, ref, alt])+'\n')
                        ref_fasta.write('>' + str(counter) + '\n')
                        ref_fasta.write(ref_seq + '\n')
                        alt_fasta.write('>' + str(counter) + '\n')
                        alt_fasta.write(alt_seq + '\n')
                        counter += 1
