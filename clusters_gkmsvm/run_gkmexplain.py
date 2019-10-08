import os
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main(args):
    if args[1] == 'all':
        for split in range(10):
            chunk(args[0], str(split), args[2], args[3])
    else:
        chunk(args[0], args[1], args[2], args[3])
    setup_pool(args[0], args[1], args[4])
    if args[1] == 'all':
        for split in range(10):
            major,minor = concat(args[0], str(split))
            to_file(args[0], str(split), major, minor, args[2], args[3])
    else:
        major,minor = concat(args[0], args[1])
        to_file(args[0], args[1], major, minor, args[2], args[3])


def chunk(cluster, fold, gwas, peak):
    major_in = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/gwas/'+peak+'/'+gwas+'.major.fasta'
    minor_in = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/gwas/'+peak+'/'+gwas+'.minor.fasta'
    for old_major_infile in os.listdir('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/input/major/'):
        os.remove('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/input/major/'+old_major_infile)
    for old_minor_infile in os.listdir('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/input/minor/'):
        os.remove('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/input/minor/'+old_minor_infile)
    for old_major_outfile in os.listdir('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/output/major/'):
        os.remove('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/output/major/'+old_major_outfile)
    for old_minor_outfile in os.listdir('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/output/minor/'):
        os.remove('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/output/minor/'+old_minor_outfile)
    with open(major_in) as inf:
        lines = inf.readlines()
        for i in range(0, len(lines), 2):
            if (len(lines) - i) < 2:
                sublines = lines[i:]
            else:
                sublines = lines[i:(i+2)]
            with open('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/input/major/input_'+str(i//2), 'w') as outf:
                for line in sublines:
                    outf.write(line)
    with open(minor_in) as inf:
        lines = inf.readlines()
        for i in range(0, len(lines), 2):
            if (len(lines) - i) < 2:
                sublines = lines[i:]
            else:
                sublines = lines[i:(i+2)]
            with open('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/input/minor/input_'+str(i//2), 'w') as outf:
                for line in sublines:
                    outf.write(line)


def setup_pool(cluster, fold, workers):
    pool_inputs = []
    if fold == 'all':
        for split in range(10):
            major_dir_in = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+str(split)+'/explain/input/major/'
            minor_dir_in = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+str(split)+'/explain/input/minor/'
            model = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+str(split)+'/train/train.output.model.txt'
            major_dir_out = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+str(split)+'/explain/output/major/'
            minor_dir_out = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+str(split)+'/explain/output/minor/'
            for infile in os.listdir(major_dir_in):
                pool_inputs.append((major_dir_in + infile, model, major_dir_out + 'output_' + infile.split('_')[1]))
            for infile in os.listdir(minor_dir_in):
                pool_inputs.append((minor_dir_in + infile, model, minor_dir_out + 'output_' + infile.split('_')[1]))
    else:
        major_dir_in = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/input/major/'
        minor_dir_in = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/input/minor/'
        model = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/train/train.output.model.txt'
        major_dir_out = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/output/major/'
        minor_dir_out = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/output/minor/'
        for infile in os.listdir(major_dir_in):
            pool_inputs.append((major_dir_in + infile, model, major_dir_out + 'output_' + infile.split('_')[1]))
        for infile in os.listdir(minor_dir_in):
            pool_inputs.append((minor_dir_in + infile, model, minor_dir_out + 'output_' + infile.split('_')[1]))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        merge=pool.map(run_explain, pool_inputs)


def run_explain(inputs):
    os.system('/users/soumyak/lsgkm/src/gkmexplain -m 1 ' + inputs[0] + ' ' + inputs[1] + ' ' + inputs[2])


def concat(cluster, fold):
    major_catted = []
    minor_catted = []
    for i in range(len(os.listdir('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/output/major/'))):
        with open('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/output/major/output_'+str(i)) as inf:
            lines = inf.readlines()
            major_catted += lines
    for i in range(len(os.listdir('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/output/minor/'))):
        with open('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/output/minor/output_'+str(i)) as inf:
            lines = inf.readlines()
            minor_catted += lines
    return major_catted, minor_catted


def to_file(cluster, fold, major, minor, gwas, peak):
    with open('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/output/'+gwas+'_'+peak+'_major_hyp_scores.txt', 'w') as outf:
        for line in major:
            outf.write(line)
    with open('/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+fold+'/explain/output/'+gwas+'_'+peak+'_minor_hyp_scores.txt', 'w') as outf:
        for line in minor:
            outf.write(line)


if __name__ == "__main__":
    cluster = sys.argv[1]
    fold = sys.argv[2]
    gwas = sys.argv[3]
    peak = sys.argv[4]
    workers = int(sys.argv[5])
    main([cluster, fold, gwas, peak, workers])
