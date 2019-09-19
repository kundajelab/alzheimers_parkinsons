import numpy as np

def one_hot_encode_along_channel_axis(sequence):
    to_return = np.zeros((len(sequence),4), dtype=np.int8)
    seq_to_one_hot_fill_in_array(zeros_array=to_return,
                                 sequence=sequence, one_hot_axis=1)
    return to_return


def seq_to_one_hot_fill_in_array(zeros_array, sequence, one_hot_axis):
    assert one_hot_axis==0 or one_hot_axis==1
    if (one_hot_axis==0):
        assert zeros_array.shape[1] == len(sequence)
    elif (one_hot_axis==1):
        assert zeros_array.shape[0] == len(sequence)
    #will mutate zeros_array
    for (i,char) in enumerate(sequence):
        if (char=="A" or char=="a"):
            char_idx = 0
        elif (char=="C" or char=="c"):
            char_idx = 1
        elif (char=="G" or char=="g"):
            char_idx = 2
        elif (char=="T" or char=="t"):
            char_idx = 3
        elif (char=="N" or char=="n"):
            continue #leave that pos as all 0's
        else:
            raise RuntimeError("Unsupported character: "+str(char))
        if (one_hot_axis==0):
            zeros_array[char_idx,i] = 1
        elif (one_hot_axis==1):
            zeros_array[i,char_idx] = 1


def normalize_scores(impscores, hyp_impscores, onehot_data):
    normed_hyp_impscores = []
    normed_impscores = []
    for i in range(len(impscores)):
        imp_score_each_pos = np.sum(impscores[i],axis=-1)
        imp_score_sign_each_pos = np.sign(imp_score_each_pos)
        hyp_scores_same_sign_mask = (np.sign(hyp_impscores[i])
                                    *imp_score_sign_each_pos[:,None] > 0)
        hyp_scores_same_sign_imp_scores_sum = np.sum(
            hyp_impscores[i]*hyp_scores_same_sign_mask,axis=-1)
        norm_ratio = imp_score_each_pos/hyp_scores_same_sign_imp_scores_sum
        norm_hyp = hyp_impscores[i]*norm_ratio[:,None]
        normed_hyp_impscores.append(norm_hyp)
        normed_impscores.append(norm_hyp*onehot_data[i])
    return normed_impscores, normed_hyp_impscores


def get_impscores(hyp_impscores, onehot_data):
    return [x*y for x,y in zip(hyp_impscores, onehot_data)]
