#!/home/groups/akundaje/soumyak/miniconda3/bin/python

import os
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main(args):
    if not os.path.isdir('/home/groups/akundaje/soumyak/alzheimers_parkinsons/scoring_new_snps/delta_scores/Cluster'+args[0]):
        os.mkdir('/home/groups/akundaje/soumyak/alzheimers_parkinsons/scoring_new_snps/delta_scores/Cluster'+args[0])
    setup_pool(args[0], int(args[1]))


def setup_pool(cluster, workers):
    basedir = '/home/groups/akundaje/soumyak/alzheimers_parkinsons/scoring_new_snps/'
    delta_pool = []
    for fold in range(10):
        effect_input = basedir + 'ism_inputs/Cluster' + cluster + '.effect.fasta'
        noneffect_input = basedir + 'ism_inputs/Cluster' + cluster + '.noneffect.fasta'
        kmer_scores = '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/kmer_scores/Cluster'+cluster+'/fold'+str(fold)+'.scores'
        kmer_output = basedir + 'delta_scores/Cluster' + cluster + '/fold' + str(fold) + '.delta.scores'
        delta_pool.append((noneffect_input, effect_input, kmer_scores, kmer_output))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        merge=pool.map(get_delta, delta_pool)


def get_delta(inputs):
    os.system('perl /home/users/soumyak/deltasvm_script/deltasvm.pl ' + inputs[0] + ' ' + inputs[1] + ' ' + inputs[2] + ' ' + inputs[3])


if __name__ == "__main__":
    cluster = sys.argv[1]
    workers = '10'
    main([cluster, workers])
