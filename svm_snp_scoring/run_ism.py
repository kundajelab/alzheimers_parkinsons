import os
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main(args):
    if not os.path.isdir('/mnt/lab_data3/soumyak/adpd/ism_scores/Cluster'+args[0]):
        os.mkdir('/mnt/lab_data3/soumyak/adpd/ism_scores/Cluster'+args[0])
    setup_pool(args[0], int(args[1]))


def setup_pool(cluster, workers):
    basedir = '/mnt/lab_data3/soumyak/adpd/'
    test_pool = []
    for fold in range(10):
        effect_fasta = basedir + 'ism_inputs/Cluster' + cluster + '.effect.fasta'
        noneffect_fasta = basedir + 'ism_inputs/Cluster' + cluster + '.noneffect.fasta'
        model = basedir + 'gkmsvm/Cluster' + cluster + '/fold' + str(fold) + '/train/train.output.model.txt'
        effect_output = basedir + 'ism_scores/Cluster' + cluster + '/fold' + str(fold) + '.effect.scores'
        noneffect_output = basedir + 'ism_scores/Cluster' + cluster + '/fold' + str(fold) + '.noneffect.scores'
        test_pool.append((effect_fasta, model, effect_output))
        test_pool.append((noneffect_fasta, model, noneffect_output))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        merge=pool.map(test_svm, test_pool)


def test_svm(inputs):
    os.system('/users/soumyak/lsgkm/src/gkmpredict -T 16 ' + inputs[0] + ' ' + inputs[1] + ' ' + inputs[2])


if __name__ == "__main__":
    cluster = sys.argv[1]
    workers = sys.argv[2]
    main([cluster, workers])
