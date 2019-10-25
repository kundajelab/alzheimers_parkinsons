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
    print("Cluster: ", cluster)
    for peak_type in ['idr', 'overlap']:
        adpd_snps = pd.read_csv('/mnt/lab_data3/soumyak/adpd/snp_lists/adpd/'+peak_type+'_intersect/Cluster'+str(cluster)+'.'+peak_type+'.adpd.snps.hg19.bed.expanded', sep='\t')
        for gwas in adpd_snps.source_gwas.unique():
            print("GWAS: ", gwas)
            gwas_snps = adpd_snps.loc[adpd_snps['source_gwas'] == gwas]
            for name in ['Kunkle', 'Jansen', 'Lambert', '23andme_PD', 'Chang', 'Nalls', 'Pankratz']:
                if name in gwas:
                    gwas_name = name
                    continue

            for fold in range(10):
                print("Fold: ", fold)
                basedir = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+str(cluster)+'/fold'+str(fold)+'/gwas/'+peak_type+'/'
                gwas_txt = open(basedir + gwas_name + '.txt', 'w')
                major_fasta = open(basedir + gwas_name + '.major.fasta', 'w')
                minor_fasta = open(basedir + gwas_name + '.minor.fasta', 'w')

                counter = 0
                for index,row in gwas_snps.iterrows():
                    chrom = row['LD_snp_chrom']
                    if chrom in hg19_splits[fold]['test']:
                        snp_start = int(row['LD_snp_0ind_pos'])
                        snp_end = int(row['LD_snp_1ind_pos'])
                        rsid = str(row['LD_rs'])

                        matches = dbsnp.query(chrom.strip('chr'), snp_start, snp_end)
                        gotmatches = False
                        for match in matches:
                            if match[2] == rsid:
                                ref = match[3]
                                if ',' in match[4]:
                                    alleles = [match[3]] + match[4].split(',')
                                else:
                                    alleles = [match[3], match[4]]
                                gotmatches = True
                                break
                        if gotmatches:
                            if 'TOPMED' in match[7] and 'CAF' in match[7]:
                                topmed_freqs = match[7].split('TOPMED=')[1].split(',')
                                topmed_max_freq = max(topmed_freqs)
                                topmed_max_ind = topmed_freqs.index(topmed_max_freq)
                                caf_freqs = match[7].split('CAF=')[1].split(';')[0].split(',')
                                caf_max_freq = max(caf_freqs)
                                caf_max_ind = caf_freqs.index(caf_max_freq)
                                #if topmed_max_ind != caf_max_ind:
                                    #print(rsid)
                                    #print(chrom, ' ', snp_start, ' ', snp_end)
                                    #print("TOPMED: ", topmed_freqs)
                                    #print("CAF: ", caf_freqs)
                                #assert topmed_max_ind == caf_max_ind
                                major = alleles[topmed_max_ind]
                                minors = alleles
                                minors.remove(major)
                            elif 'TOPMED' in match[7]:
                                topmed_freqs = match[7].split('TOPMED=')[1].split(',')
                                topmed_max_freq = max(topmed_freqs)
                                topmed_max_ind = topmed_freqs.index(topmed_max_freq)
                                major = alleles[topmed_max_ind]
                                minors = alleles
                                minors.remove(major)
                            elif 'CAF' in match[7]:
                                caf_freqs = match[7].split('CAF=')[1].split(';')[0].split(',')
                                caf_max_freq = max(caf_freqs)
                                caf_max_ind = caf_freqs.index(caf_max_freq)
                                major = alleles[caf_max_ind]
                                minors = alleles
                                minors.remove(major)
                            else:
                                major = alleles[0]
                                minors = alleles
                                minors.remove(major)

                            start = snp_end - 500
                            end = snp_end + 500
                            seq = ref_gen.fetch(chrom, start, end)
                            seq = seq.upper()
                            major_right = seq[500:]
                            major_left = seq[:(500-len(major))]
                            major_seq = major_left + major + major_right
                            if len(major_seq) < 1000:
                                major_seq += ref_gen.fetch(chrom, end, end + 1000 - len(major_seq))
                            else:
                                major_seq = major_seq[:1000]
                            i = 1
                            if major == ref:
                                while seq != major_seq and i < 2:
                                    start = snp_end - i - 500
                                    end = snp_end - i + 500
                                    seq = ref_gen.fetch(chrom, start, end)
                                    seq = seq.upper()
                                    major_right = seq[500:]
                                    major_left = seq[:(500-len(major))]
                                    major_seq = major_left + major + major_right
                                    if len(major_seq) < 1000:
                                        major_seq += ref_gen.fetch(chrom, end, end + 1000 - len(major_seq))
                                    else:
                                        major_seq = major_seq[:1000]
                                    i += 1
                                if len(major) > 1 and seq != major_seq:
                                    continue
                                assert seq == major_seq, '\n' + '\n'.join(['Ref Seq: '+seq[490:510], 'Major Seq: '+major_seq[490:510], 'Ref: '+ref, major_left[-10:], major_right[:10], str(snp_start), str(snp_end), 'Alt: '+minors[0]])
                                assert len(major_seq) == 1000
                            for minor in minors:
                                minor_seq = major_left + minor + major_right
                                if len(minor_seq) < 1000:
                                    minor_seq += ref_gen.fetch(chrom, end, end + 1000 - len(minor_seq))
                                else:
                                    minor_seq = minor_seq[:1000]
                                i = 1
                                if minor == ref:
                                    while seq != minor_seq and i < 2:
                                        start = snp_end - i - 500
                                        end = snp_end - i + 500
                                        seq = ref_gen.fetch(chrom, start, end)
                                        seq = seq.upper()
                                        minor_right = seq[500:]
                                        minor_left = seq[:(500-len(minor))]
                                        minor_seq = major_left + minor + major_right
                                        if len(minor_seq) < 1000:
                                            minor_seq += ref_gen.fetch(chrom, end, end + 1000 - len(minor_seq))
                                        else:
                                            minor_seq = minor_seq[:1000]
                                        i += 1
                                    if len(minor) > 1 and seq != minor_seq:
                                        continue
                                    assert seq == minor_seq, '\n' + '\n'.join(['Ref Seq: '+seq[490:510], 'Minor Seq: '+minor_seq[490:510], 'Ref: '+ref, minor_left[-10:], minor_right[:10], str(snp_start), str(snp_end), 'Alt: '+major])
                                    assert len(minor_seq) == 1000

                                assert major_seq != minor_seq, '\n' + '\n'.join(['Major Seq: '+major_seq[490:510], 'Minor Seq: '+minor_seq[490:510], 'Major: ' +major, 'Minor: ' + minor, str(snp_start), str(snp_end)])
                                assert len(minor_seq) == 1000
                                gwas_txt.write('\t'.join([str(i) for i in row]+[major, minor])+'\n')
                                major_fasta.write('>' + str(counter) + '\n')
                                major_fasta.write(major_seq + '\n')
                                minor_fasta.write('>' + str(counter) + '\n')
                                minor_fasta.write(minor_seq + '\n')
                                counter += 1
                                if counter % 1000 == 0:
                                    print("Counter: ", counter)
