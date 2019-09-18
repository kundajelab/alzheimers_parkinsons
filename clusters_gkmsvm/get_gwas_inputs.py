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
    #ld_snps = '/mnt/lab_data2/annashch/alzheimers_parkinsons/cluster_enrichment_for_gwas_hits/intersections/intersection.Kunkle.idr.clusters.Cluster'+str(cluster)+'.idr.optimal.narrowPeak'
    ld_snps = '/mnt/lab_data2/annashch/alzheimers_parkinsons/cluster_enrichment_for_gwas_hits/intersections/intersection.23andme.idr.clusters.Cluster'+str(cluster)+'.idr.optimal.narrowPeak'
    ld = pd.read_csv(ld_snps, header=None, sep='\t')
    ld = ld[[3, 4, 5, 6]]
    ld.rename(columns={3:'chrom', 4:'start', 5:'end', 6:'rsid'}, inplace=True)
    for fold in range(10):
        print("Fold: ", fold)
        basedir = '/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+str(cluster)+'/fold'+str(fold)+'/test/'
        #gwas_bed = open(basedir + 'gwas.pos.bed', 'w')
        #ref_fasta = open(basedir + 'ref.pos.fasta', 'w')
        #alt_fasta = open(basedir + 'alt.pos.fasta', 'w')
        gwas_bed = open(basedir + 'pd_gwas.pos.bed', 'w')
        ref_fasta = open(basedir + 'pd_ref.pos.fasta', 'w')
        alt_fasta = open(basedir + 'pd_alt.pos.fasta', 'w')
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
                        if ',' in match[4]:
                            alts = match[4].split(',')
                        else:
                            alts = [match[4]]
                        gotmatches = True
                        break
                if gotmatches:
                    start = snp_end - 500
                    end = snp_end + 500
                    seq = ref_gen.fetch(chrom, start, end)
                    seq = seq.upper()
                    if 'N' in seq:
                        continue
                    ref_right = seq[500:]
                    ref_left = seq[:(500-len(ref))]
                    ref_seq = ref_left + ref + ref_right
                    i = 1
                    while seq != ref_seq and i < 100:
                        start = snp_end - i - 500
                        end = snp_end - i + 500
                        seq = ref_gen.fetch(chrom, start, end)
                        seq = seq.upper()
                        if 'N' in seq:
                            continue
                        ref_right = seq[500:]
                        ref_left = seq[:(500-len(ref))]
                        ref_seq = ref_left + ref + ref_right
                        i += 1
                    if len(ref) > 1 and seq != ref_seq:
                        continue
                    assert seq == ref_seq, '\n' + '\n'.join(['My Seq: '+seq[490:510], 'Rf Seq: '+ref_seq[490:510], 'ref: '+ref, ref_left[-10:], ref_right[:10], str(snp_start), str(snp_end), 'alt: '+alt])
                    assert len(ref_seq) == 1000
                    for alt in alts:
                        alt_seq = ref_left + alt + ref_right
                        if len(alt_seq) < 1000:
                            alt_seq += ref_gen.fetch(chrom, end, end + 1000 - len(alt_seq))
                        else:
                            alt_seq = alt_seq[:1000]
                        assert alt_seq != ref_seq, '\n' + '\n'.join(['Ref Seq: '+ref_seq[490:510], 'Alt Seq: '+alt_seq[490:510], 'ref: ' +ref, 'alt: ' + alt, str(snp_start), str(snp_end)])
                        assert len(alt_seq) == 1000
                        gwas_bed.write('\t'.join([chrom, str(snp_start), str(snp_end), rsid, ref, alt])+'\n')
                        ref_fasta.write('>' + str(counter) + '\n')
                        ref_fasta.write(ref_seq + '\n')
                        alt_fasta.write('>' + str(counter) + '\n')
                        alt_fasta.write(alt_seq + '\n')
                        counter += 1
