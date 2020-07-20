import os
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main(args):
    for i in range(1, 25):
        if not os.path.isdir('/mnt/lab_data3/soumyak/adpd/delta_scores/Cluster'+str(i)):
            os.mkdir('/mnt/lab_data3/soumyak/adpd/delta_scores/Cluster'+str(i))
        setup_pool(str(i), 40)


def setup_pool(cluster, workers):
    basedir = '/mnt/lab_data3/soumyak/adpd/'
    delta_pool = []
    for fold in range(10):
        effect_input = basedir + 'ism_inputs/Cluster'+cluster+'.effect.fasta'
        noneffect_input = basedir + 'ism_inputs/Cluster'+cluster+'.noneffect.fasta'
        kmer_scores = basedir + 'kmer_scores/Cluster'+cluster+'/fold'+str(fold)+'.scores'
        kmer_output = basedir + 'delta_scores/Cluster' + cluster + '/fold' + str(fold) + '.delta.scores'
        delta_pool.append((noneffect_input, effect_input, kmer_scores, kmer_output))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        merge=pool.map(get_delta, delta_pool)


def get_delta(inputs):
    os.system('perl /users/soumyak/deltasvm_script/deltasvm.pl ' + inputs[0] + ' ' + inputs[1] + ' ' + inputs[2] + ' ' + inputs[3])


if __name__ == "__main__":
    main(sys.argv[1:])
