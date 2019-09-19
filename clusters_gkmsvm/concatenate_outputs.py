import os
import sys


def main(args):
    if args[1] == 'all':
        for split in range(10):
            ref,alt = concat(args[0], str(split))
            to_file(args[0], str(split), ref, alt)
    else:
        ref,alt = concat(args[0], args[1])
        to_file(args[0], args[1], ref, alt)


def concat(cluster, fold):
    ref_catted = []
    alt_catted = []
    for i in range(len(os.listdir('/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+cluster+'/fold'+fold+'/explain/output/ref/'))):
        with open('/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+cluster+'/fold'+fold+'/explain/output/ref/output_'+str(i)) as inf:
            lines = inf.readlines()
            ref_catted += lines
    for i in range(len(os.listdir('/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+cluster+'/fold'+fold+'/explain/output/alt/'))):
        with open('/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+cluster+'/fold'+fold+'/explain/output/alt/output_'+str(i)) as inf:
            lines = inf.readlines()
            alt_catted += lines
    return ref_catted, alt_catted


def to_file(cluster, fold, ref, alt):
    with open('/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+cluster+'/fold'+fold+'/explain/output/ref_hyp_scores.txt', 'w') as outf:
        for line in ref:
            outf.write(line)
    with open('/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+cluster+'/fold'+fold+'/explain/output/alt_hyp_scores.txt', 'w') as outf:
        for line in alt:
            outf.write(line)


if __name__ == "__main__":
    main(sys.argv[1:])
