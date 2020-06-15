import os
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main(args):
    if not os.path.isdir('/home/groups/akundaje/soumyak/alzheimers_parkinsons/scoring_new_snps/explain_scores/Cluster'+args[0]):
        os.mkdir('/home/groups/akundaje/soumyak/alzheimers_parkinsons/scoring_new_snps/explain_scores/Cluster'+args[0])
    setup_pool(args[0], args[1], int(args[2]))


def setup_pool(cluster, fold, workers):
    basedir = '/home/groups/akundaje/soumyak/alzheimers_parkinsons/scoring_new_snps/'
    test_pool = []
    effect_fasta = basedir + 'explain_inputs/Cluster' + cluster + '.effect.fasta'
    noneffect_fasta = basedir + 'explain_inputs/Cluster' + cluster + '.noneffect.fasta'
    model = '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/svm_models/Cluster' + cluster + '/fold' + str(fold) + '.model.txt'
    effect_output = basedir + 'explain_scores/Cluster' + cluster + '/fold' + str(fold) + '.effect.scores'
    noneffect_output = basedir + 'explain_scores/Cluster' + cluster + '/fold' + str(fold) + '.noneffect.scores'
    test_pool.append((effect_fasta, model, effect_output))
    test_pool.append((noneffect_fasta, model, noneffect_output))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        merge=pool.map(test_svm, test_pool)


def test_svm(inputs):
    os.system('/home/groups/akundaje/soumyak/lsgkm/src/gkmexplain ' + inputs[0] + ' ' + inputs[1] + ' ' + inputs[2])


if __name__ == "__main__":
    cluster = sys.argv[1]
    fold = sys.argv[2]
    workers = '1'#sys.argv[3]
    main([cluster, fold, workers])
