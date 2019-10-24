import sys
import pysam
import pybedtools
import numpy as np
import pandas as pd


ref_fasta = '/mnt/lab_data3/soumyak/refs/hg19/male.hg19.fa'
ref_gen = pysam.FastaFile(ref_fasta)


def main(args):
    for gwas in ['Kunkle']:
        print("GWAS: ", gwas)
        for cluster in range(1, 25):
            print("Cluster: ", str(cluster))
            snps = pd.read_csv('/mnt/lab_data3/soumyak/adpd/snp_lists/'+gwas+'/expanded/Cluster'+str(cluster)+'.overlap.expanded.snps.hg19.bed', sep='\t')
            make_fasta(snps, gwas, str(cluster))


def make_fasta(snps, gwas, cluster):
    major_fasta = open('/mnt/lab_data3/soumyak/adpd/fasta_inputs/'+gwas+'/Cluster'+cluster+'.major.fasta', 'w')
    minor_fasta = open('/mnt/lab_data3/soumyak/adpd/fasta_inputs/'+gwas+'/Cluster'+cluster+'.minor.fasta', 'w')
    counter = 0
    for index, row in snps.iterrows():
        chrom = row['ld_chr']
        start = row['ld_end'] - 500
        end = row['ld_end'] + 500
        rsid = row['ld_rsid']
        major = row['major']
        minor = row['minor']
        seq = ref_gen.fetch(chrom, start, end)
        seq = seq.upper()
        major_right = seq[500:]
        major_left = seq[:(500-len(major))]
        major_seq = major_left + major + major_right
        if len(major_seq) < 1000:
            major_seq += ref_gen.fetch(chrom, end, end + 1000 - len(major_seq))
        else:
            major_seq = major_seq[:1000]
        minor_seq = major_left + minor + major_right
        if len(minor_seq) < 1000:
            minor_seq += ref_gen.fetch(chrom, end, end + 1000 - len(minor_seq))
        else:
            minor_seq = minor_seq[:1000]
        assert len(major_seq) == 1000
        assert len(minor_seq) == 1000
        assert major_seq != minor_seq
        if row['major'] == row['ref']:
            assert seq == major_seq, '\n' + '\n'.join([seq[490:510], major_seq[490:510], major])
        if row['minor'] == row['ref']:
            assert seq == minor_seq
        for i,j in snps.iterrows():
            if j['ld_chr'] == chrom and j['ld_rsid'] != rsid and j['ld_rsid'] != '.' and j['ld_start'] >= start and j['ld_end'] <= end and len(j['minor']) == 1 and len(j['major']) == 1:
                offset = j['ld_start'] - start
                major_seq = major_seq[:offset] + j['major'] + major_seq[(offset+1):]
                minor_seq = minor_seq[:offset] + j['minor'] + minor_seq[(offset+1):]
        assert len(major_seq) == 1000
        assert len(minor_seq) == 1000
        assert major_seq != minor_seq
        major_fasta.write('>' + str(counter) + '\n')
        major_fasta.write(major_seq + '\n')
        minor_fasta.write('>' + str(counter) + '\n')
        minor_fasta.write(minor_seq + '\n')
        counter += 1


if __name__ == "__main__":
    main(sys.argv[1:])
