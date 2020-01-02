import sys
import math
import statistics
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import *
from decimal import Decimal
from IPython.display import Image
from matplotlib import pyplot as plt

sys.path.insert(0, '/users/soumyak/alzheimers_parkinsons/clusters_gkmsvm')
from viz_preprocess import *
from viz_sequence import *
from make_plots import *
from kerasAC.splits import *


def main(args):
    cluster = args[0]
    cluster_input = int(args[0])
    effect_scores = {}
    noneffect_scores = {}
    ism_scores = {}
    delta_scores = {}
    prep_scores(cluster, effect_scores, noneffect_scores, ism_scores, delta_scores)
    sig_list = {}
    ksvals = {}
    motifs = {}
    motif_others = {}
    get_imp_dist(cluster, sig_list, ksvals, motifs, motif_others, effect_scores, noneffect_scores)


def prep_scores(cluster, effect_scores, noneffect_scores, ism_scores, delta_scores):
    effect_fasta = '/mnt/lab_data3/soumyak/adpd/fasta_inputs/Cluster' \
                    +cluster+'.effect.fasta'
    effect_seqs = [x.rstrip() for (i,x) in enumerate(open(effect_fasta)) if i%2==1]
    effect_onehot = [np.array(one_hot_encode_along_channel_axis(x)) for x in effect_seqs]
    print("Num effect sequences:", '\t', '\t', len(effect_onehot))

    noneffect_fasta = '/mnt/lab_data3/soumyak/adpd/fasta_inputs/Cluster' \
                       +cluster+'.noneffect.fasta'
    noneffect_seqs = [x.rstrip() for (i,x) in enumerate(open(noneffect_fasta)) if i%2==1]
    noneffect_onehot = [np.array(one_hot_encode_along_channel_axis(x)) for x in noneffect_seqs]
    print("Num noneffect sequences:", '\t', len(noneffect_onehot))

    for fold in range(10):
        effect_file = '/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster' \
                       +cluster+'/fold'+str(fold)+'.effect.scores.txt'
        effect_scores[fold] = get_hyp_scores(effect_file, effect_seqs)
        effect_scores[fold] = np.array(effect_scores[fold])

        noneffect_file = '/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster' \
                          +cluster+'/fold'+str(fold)+'.noneffect.scores.txt'
        noneffect_scores[fold] = get_hyp_scores(noneffect_file, noneffect_seqs)
        noneffect_scores[fold] = np.array(noneffect_scores[fold])

        ism_scores[fold] = np.array([float(i.strip().split('\t')[1]) \
                                     for i in open('/mnt/lab_data3/soumyak/adpd/ism_scores/Cluster'
                                                   +cluster+'/fold'+str(fold)+'.ism.scores').readlines()])
        delta_scores[fold] = np.array([float(i.strip().split('\t')[1]) \
                                       for i in open('/mnt/lab_data3/soumyak/adpd/delta_scores/Cluster'
                                                      +cluster+'/fold'+str(fold)+'.delta.scores').readlines()])


def get_imp_scores(cluster, sig_list, ksvals, motifs, motif_others, effect_scores, noneffect_scores):
    


if __name__ == '__main__':
    main(sys.argv[1:])
