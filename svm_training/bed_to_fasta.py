import sys
import pysam
import pandas as pd


def main(args):
    get_seqs(args[0], args[1])


def get_seqs(bed, fasta):
    ref_fasta = '/mnt/lab_data3/soumyak/refs/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta'
    ref = pysam.FastaFile(ref_fasta)

    df_bed = pd.read_csv(bed, sep='\t', header=None)
    fa_file = open(fasta, 'w')

    counter = 0
    for index,row in df_bed.iterrows():
        seq=ref.fetch(row[0],int(row[1]),int(row[2]))
        fa_file.write('>' + str(counter) + '\n')
        fa_file.write(seq.upper() + '\n')
        counter += 1


if __name__ == "__main__":
    main(sys.argv[1:])

