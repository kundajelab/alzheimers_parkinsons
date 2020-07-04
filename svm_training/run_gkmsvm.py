import os
import sys
from sklearn.metrics import roc_auc_score, average_precision_score
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main(args):
    setup_pool(args[0], args[1], args[2])
    if args[1] == 'all':
        for split in range(10):
            get_acc(args[0], str(split))
    else:
        get_acc(args[0], args[1])


def setup_pool(cluster, fold, workers):
    basedir = '/mnt/lab_data3/soumyak/adpd/gkmsvm/Cluster'+cluster+'/fold'
    if fold == 'all':
        train_pool = []
        test_pool = []
        for split in range(10):
            pos_fasta = basedir + str(split) + '/train/train.final.pos.fasta'
            neg_fasta = basedir + str(split) + '/train/train.final.neg.fasta'
            output = basedir + str(split) + '/train/train.output'
            train_pool.append((pos_fasta, neg_fasta, output))
        with ProcessPoolExecutor(max_workers=workers) as pool:
            merge=pool.map(train_svm, train_pool)
        for split in range(10):
            pos_fasta = basedir + str(split) + '/test/test.final.pos.fasta'
            neg_fasta = basedir + str(split) + '/test/test.final.neg.fasta'
            model = basedir + str(split) + '/train/train.output.model.txt'
            pos_output = basedir + str(split) + '/test/test.pos.output'
            neg_output = basedir + str(split) + '/test/test.neg.output'
            test_pool.append((pos_fasta, model, pos_output))
            test_pool.append((neg_fasta, model, neg_output))
        with ProcessPoolExecutor(max_workers=workers) as pool:
            merge=pool.map(test_svm, test_pool)
    else:
        train_svm((basedir + fold + '/train/train.final.pos.fasta',
                   basedir + fold + '/train/train.final.neg.fasta',
                   basedir + fold + '/train/train.output'))
        test_svm((basedir + fold + '/test/test.final.pos.fasta',
                  basedir + fold + '/train/train.output.model.txt',
                  basedir + fold + '/test/test.pos.output'))
        test_svm((basedir + fold + '/test/test.final.neg.fasta',
                  basedir + fold + '/train/train.output.model.txt',
                  basedir + fold + '/test/test.neg.output'))


def train_svm(inputs):
    os.system('/users/soumyak/lsgkm/src/gkmtrain -T 16 ' + inputs[0] + ' ' + inputs[1] + ' ' + inputs[2])


def test_svm(inputs):
    os.system('/users/soumyak/lsgkm/src/gkmpredict -T 16 ' + inputs[0] + ' ' + inputs[1] + ' ' + inputs[2])


def get_acc(cluster, fold):
    pos_file = '/mnt/lab_data3/soumyak/adpd/gkmsvm/Cluster'+cluster+'/fold'+fold+'/test/test.pos.output'
    neg_file = '/mnt/lab_data3/soumyak/adpd/gkmsvm/Cluster'+cluster+'/fold'+fold+'/test/test.neg.output'
    pos_preds = [float(x.rstrip().split("\t")[1]) for x in open(pos_file)]
    neg_preds = [float(x.rstrip().split("\t")[1]) for x in open(neg_file)]
    with open('/mnt/lab_data3/soumyak/adpd/gkmsvm/Cluster'+cluster+'/fold'+fold+'/test/accuracy.txt', 'w') as acc_file:
        acc_file.write("Cluster: " + cluster + "; Fold: " + fold + '\n')
        acc_file.write("AUROC: " + str(roc_auc_score(y_true=[1 for x in pos_preds]+[0 for x in neg_preds],
                        y_score = pos_preds+neg_preds)) + '\n')
        acc_file.write("AUPRC: " + str(average_precision_score(y_true=[1 for x in pos_preds]+[0 for x in neg_preds],
                        y_score = pos_preds+neg_preds)) + '\n')


if __name__ == "__main__":
    cluster = sys.argv[1]
    fold = sys.argv[2]
    workers = int(sys.argv[3])
    main([cluster, fold, workers])
