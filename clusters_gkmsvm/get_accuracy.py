import sys
from sklearn.metrics import roc_auc_score, average_precision_score


def main(args):
    if args[1] == 'all':
        for split in range(10):
            get_acc(args[0], str(split))
    else:
        get_acc(args[0], args[1])


def get_acc(cluster, fold):
    pos_file = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/test/test.pos.output'
    neg_file = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/test/test.neg.output'
    pos_preds = [float(x.rstrip().split("\t")[1]) for x in open(pos_file)]
    neg_preds = [float(x.rstrip().split("\t")[1]) for x in open(neg_file)]
    with open('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/test/accuracy.txt', 'w') as acc_file:
        acc_file.write("Cluster: " + cluster + "; Fold: " + fold + '\n')
        acc_file.write("AUROC: " + str(roc_auc_score(y_true=[1 for x in pos_preds]+[0 for x in neg_preds],
                        y_score = pos_preds+neg_preds)) + '\n')
        acc_file.write("AUPRC: " + str(average_precision_score(y_true=[1 for x in pos_preds]+[0 for x in neg_preds],
                        y_score = pos_preds+neg_preds)) + '\n')


if __name__ == "__main__":
    main(sys.argv[1:])
