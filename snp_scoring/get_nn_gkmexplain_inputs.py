import sys
import pysam
import pybedtools
import numpy as np
import pandas as pd


snp_file = '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/snps_final/ld_buddies_table_stage2_2019-10-25.tsv'
nn_file = '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dl_svm_combined_snp_tracks/nn_hits_missed_by_svm/nn_unique_annotated.txt'
ref_fasta = '/mnt/lab_data3/soumyak/refs/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta'
ref_gen = pysam.FastaFile(ref_fasta)


def main(args):
    get_coords(snp_file, nn_file)
    nn_snps = pd.read_csv('/mnt/lab_data3/soumyak/adpd/nn_analysis/nn_only_snps.bed', sep='\t')
    make_fasta(nn_snps)

def get_coords(snp_file, nn_file):
    all_snps = pd.read_csv(snp_file, sep='\t')
    nn_snps = pd.read_csv(nn_file, sep='\t')
    all_snps['chr'] = all_snps['chr'].apply(lambda x : 'chr' + str(x))
    all_snps.rename(columns = {'pos': 'end'}, inplace=True)
    nn_snps.rename(columns = {'snp': 'rsid'}, inplace=True)
    all_snps['start'] = all_snps['end'] - 1
    all_snps = all_snps[['chr', 'start', 'end', 'rsid']]
    merged_snps = nn_snps.merge(all_snps, on='rsid')
    merged_snps.drop_duplicates(inplace=True)
    merged_snps = merged_snps[['chr', 'start', 'end', 'rsid', 'effect', 'noneffect', 'cluster', 'fold']]
    merged_snps.sort_values(by=['cluster', 'fold'], inplace=True)
    merged_snps.to_csv('/mnt/lab_data3/soumyak/adpd/nn_analysis/nn_only_snps.bed', sep='\t', index=False)

def make_fasta(nn_snps):
    effect_fasta = open('/mnt/lab_data3/soumyak/adpd/nn_analysis/nn.effect.fasta', 'w')
    noneffect_fasta = open('/mnt/lab_data3/soumyak/adpd/nn_analysis/nn.noneffect.fasta', 'w')
    counter = 0
    for index, row in nn_snps.iterrows():
        chrom = row['chr']
        start = row['end'] - 500
        end = row['end'] + 500
        rsid = row['rsid']
        effect = row['effect']
        noneffect = row['noneffect']
        seq = ref_gen.fetch(chrom, start, end)
        seq = seq.upper()
        effect_right = seq[500:]
        effect_left = seq[:(500-len(effect))]
        effect_seq = effect_left + effect + effect_right
        if len(effect_seq) < 1000:
            effect_seq += ref_gen.fetch(chrom, end, end + 1000 - len(effect_seq))
        else:
            effect_seq = effect_seq[:1000]
        noneffect_seq = effect_left + noneffect + effect_right
        if len(noneffect_seq) < 1000:
            noneffect_seq += ref_gen.fetch(chrom, end, end + 1000 - len(noneffect_seq))
        else:
            noneffect_seq = noneffect_seq[:1000]
        assert len(effect_seq) == 1000
        assert len(noneffect_seq) == 1000
        if effect != 'N':
            assert effect_seq != noneffect_seq
        effect_fasta.write('>' + str(counter) + '\n')
        effect_fasta.write(effect_seq + '\n')
        noneffect_fasta.write('>' + str(counter) + '\n')
        noneffect_fasta.write(noneffect_seq + '\n')
        counter += 1


if __name__ == "__main__":
    main(sys.argv[1:])
