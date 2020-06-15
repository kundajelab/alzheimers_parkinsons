import os
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main(args):
    if not os.path.isdir('/home/soumyak/kmer_scores/Cluster'+args[0]):
        os.mkdir('/home/soumyak/kmer_scores/Cluster'+args[0])
    setup_pool(args[0], int(args[1]))


def setup_pool(cluster, workers):
    basedir = '/home/soumyak/'
    test_pool = []
    for fold in range(10):
        kmers = basedir + 'kmers.txt'
        model = basedir + 'clusters_gkmsvm/Cluster' + cluster + '/fold' + str(fold) + '/train/train.output.model.txt'
        kmer_output = basedir + 'kmer_scores/Cluster' + cluster + '/fold' + str(fold) + '.scores'
        test_pool.append((kmers, model, kmer_output))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        merge=pool.map(test_svm, test_pool)


def test_svm(inputs):
    os.system('/users/soumyak/lsgkm/src/gkmpredict -T 16 ' + inputs[0] + ' ' + inputs[1] + ' ' + inputs[2])


if __name__ == "__main__":
    cluster = sys.argv[1]
    workers = sys.argv[2]
    main([cluster, workers])
