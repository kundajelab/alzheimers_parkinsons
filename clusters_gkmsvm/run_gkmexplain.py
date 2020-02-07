import os
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main(args):
    if not os.path.isdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+args[0]):
        os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+args[0])
        os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+args[0]+'/input')
        os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+args[0]+'/input/effect')
        os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+args[0]+'/input/noneffect')
        os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+args[0]+'/output')
        os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+args[0]+'/output/effect')
        os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+args[0]+'/output/noneffect')
        for fold in range(10):
            os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+args[0]+'/output/effect/fold'+str(fold))
            os.mkdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+args[0]+'/output/noneffect/fold'+str(fold))
    chunk(args[0], int(args[1]))
    setup_pool(args[0], int(args[1]))
    for fold in range(10):
        effect,noneffect = concat(args[0], str(fold))
        to_file(args[0], str(fold), effect, noneffect)


def chunk(cluster, workers):
    effect_in = '/mnt/lab_data3/soumyak/adpd/fasta_inputs/Cluster'+cluster+'.effect.fasta'
    noneffect_in = '/mnt/lab_data3/soumyak/adpd/fasta_inputs/Cluster'+cluster+'.noneffect.fasta'
    for old_effect_infile in os.listdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/input/effect/'):
        os.remove('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/input/effect/'+old_effect_infile)
    for old_noneffect_infile in os.listdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/input/noneffect/'):
        os.remove('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/input/noneffect/'+old_noneffect_infile)
    for fold in range(10):
        for old_effect_outfile in os.listdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/output/effect/fold'+str(fold)+'/'):
            os.remove('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/output/effect/fold'+str(fold)+'/'+old_effect_outfile)
        for old_noneffect_outfile in os.listdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/output/noneffect/fold'+str(fold)+'/'):
            os.remove('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/output/noneffect/fold'+str(fold)+'/'+old_noneffect_outfile)
    with open(effect_in) as inf:
        lines = inf.readlines()
        perfile = len(lines) // workers
        perfile = perfile - (perfile % 2)
        assert perfile % 2 == 0
        for i in range(0, len(lines), perfile):
            if (len(lines) - i) < perfile:
                sublines = lines[i:]
            else:
                sublines = lines[i:(i+perfile)]
            with open('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/input/effect/input_'+str(i//perfile), 'w') as outf:
                for line in sublines:
                    outf.write(line)
    with open(noneffect_in) as inf:
        lines = inf.readlines()
        perfile = len(lines) // workers
        perfile = perfile - (perfile % 2)
        assert perfile % 2 == 0
        for i in range(0, len(lines), perfile):
            if (len(lines) - i) < perfile:
                sublines = lines[i:]
            else:
                sublines = lines[i:(i+perfile)]
            with open('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/input/noneffect/input_'+str(i//perfile), 'w') as outf:
                for line in sublines:
                    outf.write(line)


def setup_pool(cluster, workers=50):
    pool_inputs = []
    for fold in range(10):
        effect_dir_in = '/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/input/effect/'
        noneffect_dir_in = '/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/input/noneffect/'
        model = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+cluster+'/fold'+str(fold)+'/train/train.output.model.txt'
        effect_dir_out = '/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/output/effect/fold'+str(fold)+'/'
        noneffect_dir_out = '/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/output/noneffect/fold'+str(fold)+'/'
        for infile in os.listdir(effect_dir_in):
            pool_inputs.append((effect_dir_in + infile, model, effect_dir_out + 'output_' + infile.split('_')[1]))
        for infile in os.listdir(noneffect_dir_in):
            pool_inputs.append((noneffect_dir_in + infile, model, noneffect_dir_out + 'output_' + infile.split('_')[1]))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        merge=pool.map(run_explain, pool_inputs)


def run_explain(inputs):
    os.system('/users/soumyak/lsgkm/src/gkmexplain ' + inputs[0] + ' ' + inputs[1] + ' ' + inputs[2])


def concat(cluster, fold):
    effect_catted = []
    noneffect_catted = []
    for i in range(len(os.listdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/output/effect/fold'+fold+'/'))):
        with open('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/output/effect/fold'+fold+'/output_'+str(i)) as inf:
            lines = inf.readlines()
            effect_catted += lines
    for i in range(len(os.listdir('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/output/noneffect/fold'+fold+'/'))):
        with open('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/output/noneffect/fold'+fold+'/output_'+str(i)) as inf:
            lines = inf.readlines()
            noneffect_catted += lines
    return effect_catted, noneffect_catted


def to_file(cluster, fold, effect, noneffect):
    with open('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/fold'+fold+'.effect.scores.txt', 'w') as outf:
        for line in effect:
            outf.write(line)
    with open('/mnt/lab_data3/soumyak/adpd/explain_scores/Cluster'+cluster+'/fold'+fold+'.noneffect.scores.txt', 'w') as outf:
        for line in noneffect:
            outf.write(line)


if __name__ == "__main__":
    cluster = sys.argv[1]
    workers = sys.argv[2]
    main([cluster, workers])
