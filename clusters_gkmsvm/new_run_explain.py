import os
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main(args):
    if not os.path.isdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+args[0]+'/Cluster'+args[1]):
        os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+args[0]+'/Cluster'+args[1])
        os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+args[0]+'/Cluster'+args[1]+'/input')
        os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+args[0]+'/Cluster'+args[1]+'/input/major')
        os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+args[0]+'/Cluster'+args[1]+'/input/minor')
        os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+args[0]+'/Cluster'+args[1]+'/output')
        os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+args[0]+'/Cluster'+args[1]+'/output/major')
        os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+args[0]+'/Cluster'+args[1]+'/output/minor')
        for fold in range(10):
            os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+args[0]+'/Cluster'+args[1]+'/output/major/fold'+str(fold))
            os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+args[0]+'/Cluster'+args[1]+'/output/minor/fold'+str(fold))
    chunk(args[0], args[1])
    setup_pool(args[0], args[1], int(args[2]))
    for fold in range(10):
        major,minor = concat(args[0], args[1], str(fold))
        to_file(args[0], args[1], str(fold), major, minor)


def chunk(gwas, cluster):
    major_in = '/mnt/lab_data3/soumyak/adpd/fasta_inputs/'+gwas+'/Cluster'+cluster+'.major.fasta'
    minor_in = '/mnt/lab_data3/soumyak/adpd/fasta_inputs/'+gwas+'/Cluster'+cluster+'.minor.fasta'
    for old_major_infile in os.listdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/input/major/'):
        os.remove('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/input/major/'+old_major_infile)
    for old_minor_infile in os.listdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/input/minor/'):
        os.remove('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/input/minor/'+old_minor_infile)
    for fold in range(10):
        for old_major_outfile in os.listdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/output/major/fold'+str(fold)+'/'):
            os.remove('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/output/major/fold'+str(fold)+'/'+old_major_outfile)
        for old_minor_outfile in os.listdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/output/minor/fold'+str(fold)+'/'):
            os.remove('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/output/minor/fold'+str(fold)+'/'+old_minor_outfile)
    with open(major_in) as inf:
        lines = inf.readlines()
        for i in range(0, len(lines), 2):
            if (len(lines) - i) < 2:
                sublines = lines[i:]
            else:
                sublines = lines[i:(i+2)]
            with open('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/input/major/input_'+str(i//2), 'w') as outf:
                for line in sublines:
                    outf.write(line)
    with open(minor_in) as inf:
        lines = inf.readlines()
        for i in range(0, len(lines), 2):
            if (len(lines) - i) < 2:
                sublines = lines[i:]
            else:
                sublines = lines[i:(i+2)]
            with open('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/input/minor/input_'+str(i//2), 'w') as outf:
                for line in sublines:
                    outf.write(line)


def setup_pool(gwas, cluster, workers=50):
    pool_inputs = []
    for fold in range(10):
        major_dir_in = '/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/input/major/'
        minor_dir_in = '/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/input/minor/'
        model = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+str(fold)+'/train/train.output.model.txt'
        major_dir_out = '/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/output/major/fold'+str(fold)+'/'
        minor_dir_out = '/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/output/minor/fold'+str(fold)+'/'
        for infile in os.listdir(major_dir_in):
            pool_inputs.append((major_dir_in + infile, model, major_dir_out + 'output_' + infile.split('_')[1]))
        for infile in os.listdir(minor_dir_in):
            pool_inputs.append((minor_dir_in + infile, model, minor_dir_out + 'output_' + infile.split('_')[1]))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        merge=pool.map(run_explain, pool_inputs)


def run_explain(inputs):
    os.system('/users/soumyak/lsgkm/src/gkmexplain -m 1 ' + inputs[0] + ' ' + inputs[1] + ' ' + inputs[2])


def concat(gwas, cluster, fold):
    major_catted = []
    minor_catted = []
    for i in range(len(os.listdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/output/major/fold'+fold+'/'))):
        with open('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/output/major/fold'+fold+'/output_'+str(i)) as inf:
            lines = inf.readlines()
            major_catted += lines
    for i in range(len(os.listdir('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/output/minor/fold'+fold+'/'))):
        with open('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/output/minor/fold'+fold+'/output_'+str(i)) as inf:
            lines = inf.readlines()
            minor_catted += lines
    return major_catted, minor_catted


def to_file(gwas, cluster, fold, major, minor):
    with open('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/fold'+fold+'.major.hyp_scores.txt', 'w') as outf:
        for line in major:
            outf.write(line)
    with open('/mnt/lab_data3/soumyak/adpd/explain_scores/'+gwas+'/Cluster'+cluster+'/fold'+fold+'.minor.hyp_scores.txt', 'w') as outf:
        for line in minor:
            outf.write(line)


if __name__ == "__main__":
    gwas = sys.argv[1]
    cluster = sys.argv[2]
    workers = sys.argv[3]
    main([gwas, cluster, workers])
