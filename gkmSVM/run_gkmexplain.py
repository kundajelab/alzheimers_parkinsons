import os
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main(args):
    if args[1] == 'all':
        for split in range(10):
            chunk(args[0], str(split))
            setup_pool(args[0], str(split))
            ref,alt = concat(args[0], str(split))
            to_file(args[0], str(split), ref, alt)
    else:
        chunk(args[0], args[1])
        setup_pool(args[0], args[1])
        ref,alt = concat(args[0], args[1])
        to_file(args[0], args[1], ref, alt)


def chunk(cluster, fold):
    ref_in = '/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+cluster+'/fold'+fold+'/test/ref.pos.fasta'
    alt_in = '/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+cluster+'/fold'+fold+'/test/alt.pos.fasta'
    with open(ref_in) as inf:
        lines = inf.readlines()
        for i in range(0, len(lines), 20):
            if (len(lines) - i) < 20:
                sublines = lines[i:]
            else:
                sublines = lines[i:(i+20)]
            with open('/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+cluster+'/fold'+fold+'/explain/input/ref/input_'+str(i//20), 'w') as outf:
                for line in sublines:
                    outf.write(line)
    with open(alt_in) as inf:
        lines = inf.readlines()
        for i in range(0, len(lines), 20):
            if (len(lines) - i) < 20:
                sublines = lines[i:]
            else:
                sublines = lines[i:(i+20)]
            with open('/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+cluster+'/fold'+fold+'/explain/input/alt/input_'+str(i//20), 'w') as outf:
                for line in sublines:
                    outf.write(line)


def setup_pool(cluster, fold):
    ref_dir_in = '/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+cluster+'/fold'+fold+'/explain/input/ref/'
    alt_dir_in = '/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+cluster+'/fold'+fold+'/explain/input/alt/'
    model = '/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+cluster+'/fold'+fold+'/train/train.output.model.txt'
    ref_dir_out = '/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+cluster+'/fold'+fold+'/explain/output/ref/'
    alt_dir_out = '/mnt/lab_data3/soumyak/adpd/gkmSVM/Cluster'+cluster+'/fold'+fold+'/explain/output/alt/'
    pool_inputs = []
    for infile in os.listdir(ref_dir_in):
        pool_inputs.append((ref_dir_in + infile, model, ref_dir_out + 'output_' + infile.split('_')[1]))
    for infile in os.listdir(alt_dir_in):
        pool_inputs.append((alt_dir_in + infile, model, alt_dir_out + 'output_' + infile.split('_')[1]))
    with ProcessPoolExecutor(max_workers=40) as pool:
        merge=pool.map(run_explain, pool_inputs)


def run_explain(inputs):
    os.system('/users/soumyak/lsgkm/src/gkmexplain ' + inputs[0] + ' ' + inputs[1] + ' ' + inputs[2])


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
    cluster = sys.argv[1]
    fold = sys.argv[2]
    main([cluster, fold])
