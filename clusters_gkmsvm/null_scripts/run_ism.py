import os
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main(args):
    if not os.path.isdir('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/shuffled_ism_scores/Cluster'+args[0]):
        os.mkdir('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/shuffled_ism_scores/Cluster'+args[0])
    setup_pool(args[0], int(args[1]))


def setup_pool(cluster, workers):
    basedir = '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/'
    test_pool = []
    for fold in range(10):
        for shuffle in range(10):
            effect_fasta = basedir + 'shuffled_50bp_fasta/Cluster' + cluster + '/shuf' + str(shuffle) + '.effect.fasta'
            noneffect_fasta = basedir + 'shuffled_50bp_fasta/Cluster' + cluster + '/shuf' + str(shuffle) + '.noneffect.fasta'
            model = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster' + cluster + '/fold' + str(fold) + '/train/train.output.model.txt'
            effect_output = basedir + 'shuffled_ism_scores/Cluster' + cluster + '/fold' + str(fold) + '.shuf' + str(shuffle) + '.effect.scores'
            noneffect_output = basedir + 'shuffled_ism_scores/Cluster' + cluster + '/fold' + str(fold) + '.shuf' + str(shuffle) + '.noneffect.scores'
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
