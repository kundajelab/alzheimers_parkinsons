import sys, os, time, glob
import pdb
#sys.path.insert(0, "/users/abalsubr/DREAM-TFBS-challenge/")
import numpy as np
#from grit.lib.multiprocessing_utils import run_in_parallel
# sys.path.append('/users/abalsubr/anaconda2/lib/python2.7/site-packages')
#from src.utils import process_data

"""
From the input label file, keep the positives and replace the negatives in various ways with different class imbalances (1x, 10x, 100x):
- Flanking regions: Up to 10 bins flanking each positive bin
- Randomly sampled negatives
- GC matched randomly sampled negatives
- Dinucleotide shuffled sequences
- Motif hits
"""

#=====================================================================================================

def negs_bootstrap_samp_test(fname, neg_pos_ratio, label_suffix, random_seed=42):
    inittime = time.time()
    old_ndces = np.load(fname)
    fnparts = fname.split('/')[-1].split('.')
    np.random.seed(random_seed)
    path_pfx = process_data.array_dir
    label_arr = process_data.load_label_arr_test(fnparts[0], fnparts[1])
    samp_out = path_pfx + label_suffix + '/' + '.'.join([fnparts[0], fnparts[1], label_suffix + '_negposratio_' + str(neg_pos_ratio), 'ndx'])
    pos_ndces = np.where(label_arr == 1)[0]
    neg_ndces = np.where(label_arr == 0)[0]
    if neg_pos_ratio > 0:
        numnegs = int(neg_pos_ratio*len(pos_ndces))
    else:
        numnegs = len(neg_ndces)
    old_negs = old_ndces[len(pos_ndces):]
    new_negs = np.random.choice(old_negs, numnegs)
    np.save(samp_out, np.append(pos_ndces, new_negs).astype(int))
    print(samp_out + ' done. Time = ' + str(time.time() - inittime))


def negs_random_samp(label_arr, neg_pos_ratio, out_path, random_seed=42):
    """
    Saves an array a of indices of label_arr, so that label_arr[a] is the sampled set,
    chipseq_arr[a] is the sampled set's chipseq signal, etc (same for DNase count, motif scores, etc.).
    """
    inittime = time.time()
    np.random.seed(random_seed)
    neg_ndces = np.where(label_arr == 0)[0]
    pos_ndces = np.where(label_arr == 1)[0]
    if neg_pos_ratio > 0:
        numnegs = int(neg_pos_ratio*len(pos_ndces))
    else:
        numnegs = len(neg_ndces)
    samp_neg_ndces_ndces = np.random.choice(len(neg_ndces), numnegs)
    np.save(out_path, np.append(pos_ndces, neg_ndces[samp_neg_ndces_ndces]).astype(int))
    print(out_path + ' done. Time = ' + str(time.time() - inittime))


def negs_flanks_samp(label_arr, dummy_arg, neg_pos_ratio, compl, out_path, random_seed=42):
    inittime = time.time()
    np.random.seed(random_seed)
    neg_ndces = np.where(label_arr == 0)[0]
    pos_ndces = np.where(label_arr == 1)[0]
    amb_ndces = np.where(label_arr == -1)[0]
    edges = np.load(process_data.array_dir + 'negs_flanks/region_edge_bins_testchr.npy')
    edge_ndces = np.nonzero(edges)[0]
    if neg_pos_ratio > 0:
        numnegs = int(neg_pos_ratio*len(pos_ndces))
    else:
        numnegs = len(neg_ndces)
    neglist = np.zeros(numnegs)
    num_flank_each_side = 5
    for i in range(numnegs):
        successful = False
        while not successful:
            thisndx = np.random.choice(pos_ndces)
            list_bin_ndces = range(max(0, thisndx - num_flank_each_side), min(len(label_arr), thisndx + num_flank_each_side + 1))
            if compl:
                bitmask = np.ones(len(label_arr), dtype=bool)
                bitmask[list_bin_ndces] = False
                bitmask[pos_ndces] = False
                bitmask[amb_ndces] = False
                neglist[i] = np.random.choice(np.arange(len(label_arr))[bitmask])
                successful = True
                continue
            # Else if not compl:
            pos_bin_ndces = np.intersect1d(list_bin_ndces, pos_ndces)
            amb_bin_ndces = np.intersect1d(list_bin_ndces, amb_ndces)
            for ndx in pos_bin_ndces:
                list_bin_ndces.remove(ndx)
            for ndx in amb_bin_ndces:
                list_bin_ndces.remove(ndx)
            if i%200000 == 0:
                print(i, len(list_bin_ndces), out_path, time.time() - inittime)
            if 1 in edges[list_bin_ndces]:
                other_reg_ndces = []
                for k in range(0, 1+num_flank_each_side):
                    if ((thisndx-k) in edge_ndces):
                        np.append(other_reg_ndces, range(thisndx-num_flank_each_side, thisndx-k))
                        break
                for k in range(0, 1+num_flank_each_side):
                    if ((thisndx+k) in edge_ndces):
                        np.append(other_reg_ndces, range(thisndx+k+1, thisndx+num_flank_each_side+1))
                        break
                for n in other_reg_ndces:
                    if n in list_bin_ndces:
                        list_bin_ndces.remove(n)
            if len(list_bin_ndces) > 0:
                neglist[i] = np.random.choice(list_bin_ndces)
                successful = True
    np.save(out_path, np.append(pos_ndces, np.array(neglist)).astype(int))
    print(out_path + ' done. Time = ' + str(time.time() - inittime))


def negs_gcmatched_samp(label_arr, gc_arr, neg_pos_ratio, out_path, random_seed=42):
    np.random.seed(random_seed)
    inittime = time.time()
    good_ndces = np.where(gc_arr >= 0.0)[0]
    label_arr = label_arr[good_ndces]
    gc_arr = gc_arr[good_ndces]
    neg_ndces = np.where(label_arr == 0)[0]
    pos_ndces = np.where(label_arr == 1)[0]
    gc_negs = gc_arr[neg_ndces]
    gc_poss = gc_arr[pos_ndces]
    if neg_pos_ratio > 0:
        numnegs = int(neg_pos_ratio*len(pos_ndces))
    else:
        numnegs = len(neg_ndces)
    neglist = np.zeros(numnegs)
    numbins = 20
    bin_bds = [np.percentile(gc_poss, (100.0*(i+1))/numbins) for i in range(numbins)]
    leftofbin = np.min(gc_negs) - 1    # less than the min
    list_bin_ndces = []
    for i in range(numbins):
        ndces = np.where(np.logical_and((gc_negs <= bin_bds[i]), gc_negs > leftofbin))[0]
        leftofbin = bin_bds[i]
        list_bin_ndces.append(ndces)
    # Two steps: first sample a positive at random, then gc match it and go ahead.
    for i in range(numnegs):
        # if i%100000 == 0:
        #     print i, out_path, time.time() - inittime
        thisgc = np.random.choice(gc_poss)
        bin_ndx = min(np.searchsorted(bin_bds, thisgc), numbins-1)
        # APPROX OPTIMAL ANSWER: Pick out a subset of negatives, choose among those.
        neglist[i] = neg_ndces[np.random.choice(list_bin_ndces[bin_ndx])]
    np.save(out_path, np.append(pos_ndces, np.array(neglist)).astype(int))
    print(out_path + ' done. Time = ' + str(time.time() - inittime))
    return  np.append(pos_ndces, np.array(neglist)).astype(int)

def negs_compl_samp(label_arr, score_arr, neg_pos_ratio, compl, out_path, random_seed=42):
    np.random.seed(random_seed)
    inittime = time.time()
    neg_ndces = np.where(label_arr == 0)[0]
    pos_ndces = np.where(label_arr == 1)[0]
    score_ndces = np.where(score_arr > 0)[0] if (not compl) else np.where(score_arr <= 0)[0]
    score_neg_ndces = np.intersect1d(neg_ndces, score_ndces)
    score_pos_ndces = np.intersect1d(pos_ndces, score_ndces)
    pos_size = len(score_pos_ndces)
    numnegs = int(neg_pos_ratio*pos_size) if (neg_pos_ratio > 0) else len(score_neg_ndces)
    # print pos_size, neg_pos_ratio, numnegs, score_pos_ndces, len(score_pos_ndces)
    samp_score_neg_ndces = np.random.choice(score_neg_ndces, numnegs)
    arr_save = np.append(score_pos_ndces, samp_score_neg_ndces).astype(int)
    np.save(out_path, arr_save)
    print(out_path + ' done. Time = ' + str(time.time() - inittime))


"""
# DEPRECATED: Locality-sensitive hashing for approximate nearest neighbor search on the 16-dim dinucleotide frequency space.
# This is better with more dimensions, i.e. can be used for k-mer sequences where dimensionality naively scales exponentially in k.

from sklearn.neighbors import LSHForest
def negs_dinucmatched_samp(label_arr, dinuc_arr, neg_pos_ratio, out_path, random_seed=None):
        num_dinucs = dinuc_negs.shape[1]
        dinuc_negs_sample = np.random.choice(dinuc_negs.shape[0], min(2000000, numnegs))
        lshf = LSHForest(n_estimators=20, n_candidates=15, n_neighbors=5).fit(dinuc_negs[dinuc_negs_sample, :])
        inittime = time.time()
        for i in range(numnegs):
                # if i%100 == 0:
                #         print i, time.time() - inittime
                rand_ndx = np.random.randint(dinuc_poss.shape[0])
                query_dinuc = dinuc_poss[rand_ndx, :].reshape((1,16))
                # print query_dinuc.shape
                approx_neighbors = lshf.kneighbors(query_dinuc, return_distance=False)
                new_nbr = dinuc_negs_sample[np.random.choice(approx_neighbors[0])]
                neglist[i] = neg_ndces[new_nbr]# neg_ndces[np.random.choice(np.where(possible_indices)[0])]
        np.save(out_path, np.append(pos_ndces, np.array(neglist)).astype(int))
        print out_path + ' done. Time = ' + str(time.time() - inittime)
"""

# Depth-first quantile binning is generally fast enough.
def negs_dinucmatched_samp(label_arr, dinuc_arr, neg_pos_ratio, out_path, random_seed=42):
    np.random.seed(random_seed)
    #dinuc_arr=np.expand_dims(dinuc_arr,1)
    inittime = time.time()
    neg_ndces = np.where(label_arr == 0)[0]
    pos_ndces = np.where(label_arr == 1)[0]
    dinuc_negs = dinuc_arr[neg_ndces]
    dinuc_poss = dinuc_arr[pos_ndces]
    if neg_pos_ratio > 0:
        numnegs = int(neg_pos_ratio*len(pos_ndces))
    else:
        numnegs = len(neg_ndces)
    neglist = np.zeros(numnegs)
    numbins = 10
    num_dinucs = dinuc_negs.shape[1]
    bin_bds = []
    ndx_quantiles = []
    for j in range(num_dinucs):
        posfreqs = dinuc_poss[:,j]
        negfreqs = dinuc_negs[:,j]
        # Define the bins according to positive proposal dist.
        pcts = [np.percentile(posfreqs, (100.0*(i+1))/numbins) for i in range(numbins)]
        bin_bds.append(pcts)
        leftofbin = np.min(negfreqs) - 1    # less than the min
        list_bin_ndces = []
        for i in range(numbins):   # bin negatives
            ndces = np.where(np.logical_and(negfreqs <= pcts[i], negfreqs > leftofbin))[0]
            leftofbin = pcts[i]
            list_bin_ndces.append(ndces)
        ndx_quantiles.append(list_bin_ndces)
        print(j, time.time() - inittime)
    # First sample a positive at random, then match its most common nucleotide, then its second-most-common nucleotide, and go ahead from there.
    min_pool_size = 100
    for i in range(numnegs):
        if i%100000 == 0:
            print(i, time.time() - inittime, out_path)
        rand_ndx = np.random.randint(dinuc_poss.shape[0])
        dist_dinuc_ndces = dinuc_poss[rand_ndx, :].argsort()
        dist_dinuc = dinuc_poss[rand_ndx, :]
        possible_indices = np.ones(len(neg_ndces), dtype=bool)
        for rank_ndx in range(4):
            dinuc_ndx = dist_dinuc_ndces[-1*(1 + rank_ndx)]     # Have to flip sorted index order.
            #pdb.set_trace()
            bin_ndx = min(np.searchsorted(bin_bds[dinuc_ndx], dist_dinuc[dinuc_ndx]), numbins-1)
            ndces_to_add = ndx_quantiles[dinuc_ndx][bin_ndx]
            indicator_newposs = np.zeros(len(neg_ndces), dtype=bool)
            indicator_newposs[ndces_to_add] = True
            new_poss_indices = np.logical_and(possible_indices, indicator_newposs)
            if np.sum(new_poss_indices) >= min_pool_size:
                possible_indices = new_poss_indices
        neglist[i] = neg_ndces[np.random.choice(np.where(possible_indices)[0])]
    np.save(out_path, np.append(pos_ndces, np.array(neglist)))
    print(out_path + ' done. Time = ' + str(time.time() - inittime))
    return np.append(pos_ndces, np.array(neglist))

#=====================================================================================================
#=====================================================================================================

def save_arrays_negs(filter_name, roundstr='final', ratios=[1,10,100,0], compl=False):
    all_args = []
    inittime = time.time()
    arr = None
    if filter_name == 'negs_gcmatched':
        arr = process_data.load_gc_arr()
    elif filter_name == 'negs_dinucmatched':
        arr = process_data.load_dinuc_arr()
    for (tf, celltype) in process_data.iter_tf_ct(roundstr):
        print(tf, celltype)
        label_arr = process_data.load_label_arr_test(tf, celltype)
        if filter_name == 'negs_dhs':
            arr = process_data.load_dnase_arr(celltype)
        elif filter_name == 'negs_motif':
            if tf == 'TAF1':
                continue
            arr = process_data.load_motif_score(tf)
        for npratio in ratios:
            if not compl:
                outname = process_data.array_dir + filter_name + '/' + '.'.join([tf, celltype, filter_name + '_negposratio_' + str(npratio), 'ndx'])
            else:
                outname = process_data.array_dir + filter_name + '/' + '.'.join([tf, celltype, filter_name + '_negposratio_' + str(npratio), 'compl.ndx'])
            if filter_name in ['negs_dhs', 'negs_motif', 'negs_flanks']:
                all_args.append((label_arr, arr, npratio, compl, outname))
            elif arr is None:
                all_args.append((label_arr, npratio, outname))
            elif filter_name == 'negs_dinucmatched':
                all_args.append((label_arr, arr, npratio, outname))
    if filter_name == 'negs_random':
        run_in_parallel(16, negs_random_samp, all_args)
    elif filter_name == 'negs_gcmatched':
        run_in_parallel(16, negs_gcmatched_samp, all_args)
    elif filter_name == 'negs_dinucmatched':
        run_in_parallel(16, negs_dinucmatched_samp, all_args)
    elif filter_name == 'negs_flanks':
        run_in_parallel(16, negs_flanks_samp, all_args)
    elif (filter_name == 'negs_dhs' or filter_name == 'negs_motif'):
        run_in_parallel(16, negs_compl_samp, all_args)
    return


# Bootstrap samples the other frequencies from the dinucleotide frequency-matched ones at 10x.
def save_dinucs_bootstrap():
    all_args = []
    for samp_arr_path in glob.glob(process_data.array_dir + 'negs_dinucmatched/' + '*_10.*.npy'):
        for npratio in [1, 100, 0]:
            newpath = samp_arr_path.replace('10', str(npratio))
            if not os.path.exists(newpath):
                all_args.append((samp_arr_path, npratio, 'negs_dinucmatched'))
    run_in_parallel(16, negs_bootstrap_samp_test, all_args)
    return


#=====================================================================================================

# TODO: Finish implementing flanks complement, add its perf graphs.
# import eval_utils

if __name__ == "__main__":
    tmprats = [1, 10, 100, 0]
    #tmprats = [0]
    roundstr='final'
    # save_arrays_negs('negs_dinucmatched', roundstr=roundstr, ratios=[10])
    save_dinucs_bootstrap()
    # save_arrays_negs('negs_flanks', roundstr=roundstr, ratios=tmprats)

    allargs = []
    for roundstr in ['train', 'leader', 'final']:
        for fn in ['negs_gcmatched', 'negs_random']:#, 'negs_flanks', 'negs_dhs', 'negs_motif']:
            break
            save_arrays_negs(fn, roundstr, tmprats)
            # allargs.append((fn, roundstr, tmprats, True))
            # allargs.append((fn, roundstr, tmprats, False))
    # run_in_parallel(16, save_arrays_negs, allargs)

    ratios = [1,10,100,0]
    for roundstr in ['final2']:
        break
        # save_negs_results(roundstr, 'negs_random', ratios)
        for metric in ['auPRC']:
            for npratio in ratios:
                # eval_utils.plot_all_tasks_metrics(metric, filter_name='negs_random', roundstr=roundstr, npratio=npratio)
                pass
