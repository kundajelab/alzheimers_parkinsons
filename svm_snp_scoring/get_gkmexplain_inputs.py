import sys
import pysam
import pybedtools
import numpy as np
import pandas as pd

ref_fasta = '/mnt/lab_data3/soumyak/refs/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta'
ref_gen = pysam.FastaFile(ref_fasta)


def main(args):
    for cluster in range(1, 25):
        print("Cluster: ", str(cluster))
        snps = pd.read_csv('/mnt/lab_data3/soumyak/adpd/snp_lists/Cluster'+str(cluster)+'.overlap.expanded.snps.hg38.bed', sep='\t')
        make_fasta(snps, str(cluster))


def make_fasta(snps, cluster):
    effect_fasta = open('/mnt/lab_data3/soumyak/adpd/explain_inputs/Cluster'+cluster+'.effect.fasta', 'w')
    noneffect_fasta = open('/mnt/lab_data3/soumyak/adpd/explain_inputs/Cluster'+cluster+'.noneffect.fasta', 'w')
    counter = 0
    for index, row in snps.iterrows():
        chrom = row['chr']
        start = row['end'] - 100
        end = row['end'] + 100
        rsid = row['rsid']
        ref = row['ref']
        alt = row['alt']
        major = row['major']
        minor = row['minor']
        effect = row['effect']
        noneffect = row['noneffect']
        if (effect == 'NAN' or effect == 'I' or effect == 'D') or (noneffect == 'NAN' or noneffect == 'I' or noneffect == 'D'):
            if (major != '.') and (minor.split(',')[0] != '.'):
                effect = minor.split(',')[0]
                noneffect = major
            elif (ref != '.') and (alt.split(',')[0] != '.'):
                effect = alt.split(',')[0]
                noneffect = ref
            else:
                effect = 'N'
                noneffect = 'N'
        seq = ref_gen.fetch(chrom, start, end)
        seq = seq.upper()
        if effect == row['ref']:
            effect_right = seq[100:]
            effect_left = seq[:(100-len(effect))]
            effect_seq = effect_left + effect + effect_right
            if len(effect_seq) < 200:
                effect_seq += ref_gen.fetch(chrom, end, end + 200 - len(effect_seq))
            else:
                effect_seq = effect_seq[:200]
            noneffect_seq = effect_left + noneffect + effect_right
            if len(noneffect_seq) < 200:
                noneffect_seq += ref_gen.fetch(chrom, end, end + 200 - len(noneffect_seq))
            else:
                noneffect_seq = noneffect_seq[:200]
        else:
            noneffect_right = seq[100:]
            noneffect_left = seq[:(100-len(noneffect))]
            noneffect_seq = noneffect_left + noneffect + noneffect_right
            if len(noneffect_seq) < 200:
                noneffect_seq += ref_gen.fetch(chrom, end, end + 200 - len(noneffect_seq))
            else:
                noneffect_seq = noneffect_seq[:200]
            effect_seq = noneffect_left + effect + noneffect_right
            if len(effect_seq) < 200:
                effect_seq += ref_gen.fetch(chrom, end, end + 200 - len(effect_seq))
            else:
                effect_seq = effect_seq[:200]
        assert len(effect_seq) == 200
        assert len(noneffect_seq) == 200
        if effect != 'N':
            assert effect_seq != noneffect_seq
        if effect == row['ref']:
            assert seq == effect_seq, '\n' + '\n'.join([seq[190:210], effect_seq[190:210], effect, noneffect, rsid])
        if noneffect == row['ref']:
            assert seq == noneffect_seq, '\n' + '\n'.join([seq[190:210], noneffect_seq[190:210], noneffect, effect, rsid])
        effect_fasta.write('>' + str(counter) + '\n')
        effect_fasta.write(effect_seq + '\n')
        noneffect_fasta.write('>' + str(counter) + '\n')
        noneffect_fasta.write(noneffect_seq + '\n')
        counter += 1


if __name__ == "__main__":
    main(sys.argv[1:])
