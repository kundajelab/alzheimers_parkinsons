import os
import subprocess
import pandas as pd

bases = ['A', 'T', 'C', 'G']
all_bases = ['a', 't', 'c', 'g'] + bases
basetask = 'Cluster'
observed_basedir = '/mnt/lab_data3/soumyak/adpd/fasta_inputs/'
null_basedir = '/mnt/lab_data3/soumyak/adpd/'

for cluster in range (1, 25):
    for j in range(10):
        meme_cmd = 'fasta-shuffle-letters -kmer 2 -dna -line 1500 ' + observed_basedir \
                    + basetask + str(cluster) + '.noneffect.fasta ' + null_basedir \
                    + 'null_fasta_inputs/' \
                    + basetask + str(cluster) + '.1000bp.null' + str(j) + '.fasta'
        meme_cmd = meme_cmd.split()
        print(meme_cmd)
        ret = subprocess.call(meme_cmd)

    snps = pd.read_csv('/mnt/lab_data3/soumyak/adpd/snp_lists/'
                        + basetask + str(cluster)
                        + '.overlap.expanded.snps.hg38.bed', sep='\t')

    with open(observed_basedir + basetask + str(cluster) + '.noneffect.fasta', 'r') as noneffect_file, \
         open(observed_basedir + basetask + str(cluster) + '.effect.fasta', 'r') as effect_file:
            noneffect_seqs = noneffect_file.readlines()
            effect_seqs = effect_file.readlines()
            for index, row in snps.iterrows():
                rsid = row['rsid']
                noneffect = row['noneffect']
                effect = row['effect']
                if effect in all_bases and noneffect in all_bases and len(effect) == 1 and len(noneffect) == 1:
                    if effect.upper() in bases and noneffect.upper() in bases:
                        assert(noneffect_seqs[(2 * index) + 1][499] == noneffect)
                        assert(effect_seqs[(2 * index) + 1][499] == effect)

    len_options = [200, 50]
    len_to_score = {200: 'explain', 50: 'ism'}
    for seqlen in len_options:
        score = len_to_score[seqlen]
        print(seqlen)
        print(score)
        flank = int(seqlen / 2)
        for j in range(10):
            with open(null_basedir + 'null_fasta_inputs/' + basetask + str(cluster)
                      + '.1000bp.null' + str(j) + '.fasta', 'r') as infile, \
                 open(null_basedir + 'null_' + score + '_inputs/' + basetask + str(cluster)
                      + '.null' + str(j) + '.noneffect.fasta', 'w') as noneffect_file, \
                 open(null_basedir + 'null_' + score + '_inputs/' + basetask + str(cluster)
                      + '.null' + str(j) + '.effect.fasta', 'w') as effect_file:
                init_seqs = infile.readlines()
                for index, row in snps.iterrows():
                    rsid = row['rsid']
                    noneffect = row['noneffect']
                    effect = row['effect']
                    if effect in all_bases and noneffect in all_bases and len(effect) == 1 and len(noneffect) == 1:
                        if effect.upper() in bases and noneffect.upper() in bases:
                            noneffect_seq_name = init_seqs[(2 * index)].strip()
                            noneffect_seq = init_seqs[(2 * index) + 1][:(int(1000 / 2) - 1)] + noneffect + init_seqs[(2 * index) + 1][int(1000 / 2):]
                            noneffect_seq = noneffect_seq.strip()
                            noneffect_seq = noneffect_seq[(500 - flank):(500 + flank)]
                            effect_seq_name = init_seqs[(2 * index)].strip()
                            effect_seq = init_seqs[(2 * index) + 1][:(int(1000 / 2) - 1)] + effect + init_seqs[(2 * index) + 1][int(1000 / 2):]
                            effect_seq = effect_seq.strip()
                            effect_seq = effect_seq[(500 - flank):(500 + flank)]
                            assert len(noneffect_seq) == seqlen
                            assert len(noneffect_seq) == len(effect_seq)
                            noneffect_file.write(noneffect_seq_name + '\n')
                            noneffect_file.write(noneffect_seq + '\n')
                            effect_file.write(effect_seq_name + '\n')
                            effect_file.write(effect_seq + '\n')
        print(flank)

