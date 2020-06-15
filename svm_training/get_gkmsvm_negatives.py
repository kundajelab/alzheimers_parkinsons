import os
import sys
import bed_to_fasta
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main():
    setup_pool()


def setup_pool():
    pool_inputs = []
    for cluster in range(1,25):
        for fold in range(10):
            pool_inputs.append((cluster, fold))
    with ProcessPoolExecutor(max_workers=40) as pool:
        merge=pool.map(train_preprocess, pool_inputs)
    with ProcessPoolExecutor(max_workers=40) as pool:
        merge=pool.map(test_preprocess, pool_inputs)


def train_preprocess(inputs):
    print('[TRAIN] Cluster: ' + str(inputs[0]) + '; Fold: ' + str(inputs[1]))
    basedir = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster' + str(inputs[0]) + '/fold' + str(inputs[1]) + '/train/'
    os.system('cut -f 1,2,3 ' + basedir + 'train.pos.bed | sed -e "s/$/\t1.0/" > ' + basedir + 'train.all.bed')
    os.system("zcat " + basedir + "train.inputs.bed.gz | tail -n +2 | awk '$4 != 1.0' >> " + basedir + "train.all.bed")
    os.system('python gc_dinuc_balanced/gen_dinucleotide_freqs.py -b ' + basedir + 'train.all.bed --ratio_neg_to_pos 1.0 -o ' + basedir + 'train.gc.txt --ref_fasta /mnt/data/annotations/by_release/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta --gc')
    os.system('python gc_dinuc_balanced/gen_dinucleotide_freqs.py -b ' + basedir + 'train.all.bed --ratio_neg_to_pos 1.0 -o ' + basedir + 'train.final.bed --ref_fasta /mnt/data/annotations/by_release/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta --gc --dinuc_freq ' + basedir + 'train.gc.txt')

    pos_train = open(basedir + 'train.pos.bed')
    pos_train_len = len(pos_train.readlines())

    os.system('head -n ' + str(pos_train_len) + ' ' + basedir + 'train.final.bed.0 > ' + basedir + 'train.final.pos.bed')
    os.system('tail -n +' + str(pos_train_len + 1) + ' ' + basedir + 'train.final.bed.0 > ' + basedir + 'train.final.neg.bed')

    bed_to_fasta.get_seqs(basedir + 'train.final.pos.bed', basedir + 'train.final.pos.fasta')
    bed_to_fasta.get_seqs(basedir + 'train.final.neg.bed', basedir + 'train.final.neg.fasta')


def test_preprocess(inputs):
    print('[TEST] Cluster: ' + str(inputs[0]) + '; Fold: ' + str(inputs[1]))
    basedir = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster' + str(inputs[0]) + '/fold' + str(inputs[1]) + '/test/'
    os.system('cut -f 1,2,3 ' + basedir + 'test.pos.bed | sed -e "s/$/\t1.0/" > ' + basedir + 'test.all.bed')
    os.system("zcat " + basedir + "test.inputs.bed.gz | tail -n +2 | awk '$4 != 1.0' >> " + basedir + "test.all.bed")
    os.system('python gc_dinuc_balanced/gen_dinucleotide_freqs.py -b ' + basedir + 'test.all.bed --ratio_neg_to_pos 1.0 -o ' + basedir + 'test.gc.txt --ref_fasta /mnt/data/annotations/by_release/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta --gc')
    os.system('python gc_dinuc_balanced/gen_dinucleotide_freqs.py -b ' + basedir + 'test.all.bed --ratio_neg_to_pos 1.0 -o ' + basedir + 'test.final.bed --ref_fasta /mnt/data/annotations/by_release/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta --gc --dinuc_freq ' + basedir + 'test.gc.txt')

    pos_test = open(basedir + 'test.pos.bed')
    pos_test_len = len(pos_test.readlines())

    os.system('head -n ' + str(pos_test_len) + ' ' + basedir + 'test.final.bed.0 > ' + basedir + 'test.final.pos.bed')
    os.system('tail -n +' + str(pos_test_len + 1) + ' ' + basedir + 'test.final.bed.0 > ' + basedir + 'test.final.neg.bed')

    bed_to_fasta.get_seqs(basedir + 'test.final.pos.bed', basedir + 'test.final.pos.fasta')
    bed_to_fasta.get_seqs(basedir + 'test.final.neg.bed', basedir + 'test.final.neg.fasta')


if __name__ == "__main__":
    main()
