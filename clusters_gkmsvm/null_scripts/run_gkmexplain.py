import os
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main(args):
    if not os.path.isdir('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/shuffled_explain_scores/Cluster'+args[0]):
        os.mkdir('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/shuffled_explain_scores/Cluster'+args[0])
    setup_pool(args[0], args[1], int(args[2]))


def setup_pool(cluster, fold, workers):
    basedir = '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/'
    explain_pool = []
    for shuffle in range(10):
        effect_fasta = basedir + 'shuffled_200bp_fasta/Cluster' + cluster + '/shuf' + str(shuffle) + '.effect.fasta'
        noneffect_fasta = basedir + 'shuffled_200bp_fasta/Cluster' + cluster + '/shuf' + str(shuffle) + '.noneffect.fasta'
        model = '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/svm_models/Cluster' + cluster + '/fold' + str(fold) + '.model.txt'
        effect_output = basedir + 'shuffled_explain_scores/Cluster' + cluster + '/fold' + str(fold) + '.shuf' + str(shuffle) + '.effect.scores'
        noneffect_output = basedir + 'shuffled_explain_scores/Cluster' + cluster + '/fold' + str(fold) + '.shuf' + str(shuffle) + '.noneffect.scores'
        explain_pool.append((effect_fasta, model, effect_output))
        explain_pool.append((noneffect_fasta, model, noneffect_output))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        merge=pool.map(run_explain, explain_pool)


def run_explain(inputs):
    os.system('/home/groups/akundaje/soumyak/lsgkm/src/gkmexplain ' + inputs[0] + ' ' + inputs[1] + ' ' + inputs[2])


if __name__ == "__main__":
    cluster = sys.argv[1]
    fold = sys.argv[2]
    workers = '10'#sys.argv[3]
    main([cluster, fold, workers])
