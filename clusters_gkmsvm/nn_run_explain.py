import os
import sys
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main(args):
    chunk(int(args[0]))
    setup_pool(int(args[0]))
    effect,noneffect = concat()
    to_file(effect, noneffect)

def chunk(workers=50):
    effect_in = '/mnt/lab_data3/soumyak/adpd/nn_analysis/nn.effect.fasta'
    noneffect_in = '/mnt/lab_data3/soumyak/adpd/nn_analysis/nn.noneffect.fasta'
    for old_effect_infile in os.listdir('/mnt/lab_data3/soumyak/adpd/nn_analysis/input/effect/'):
        os.remove('/mnt/lab_data3/soumyak/adpd/nn_analysis/input/effect/'+old_effect_infile)
    for old_noneffect_infile in os.listdir('/mnt/lab_data3/soumyak/adpd/nn_analysis/input/noneffect/'):
        os.remove('/mnt/lab_data3/soumyak/adpd/nn_analysis/input/noneffect/'+old_noneffect_infile)
    nn_snps = pd.read_csv('/mnt/lab_data3/soumyak/adpd/nn_analysis/nn_only_snps.bed', sep='\t')
    with open(effect_in) as inf:
        lines = inf.readlines()
        for index, row in nn_snps.iterrows():
            print(index)
            cluster = str(row['cluster'])
            fold = str(row['fold'])
            with open('/mnt/lab_data3/soumyak/adpd/nn_analysis/input/effect/'+cluster+'_'+fold, 'a+') as outf:
                for line in lines[(index*2):(index*2)+2]:
                    outf.write(line)
    with open(noneffect_in) as inf:
        lines = inf.readlines()
        for index, row in nn_snps.iterrows():
            cluster = str(row['cluster'])
            fold = str(row['fold'])
            with open('/mnt/lab_data3/soumyak/adpd/nn_analysis/input/noneffect/'+cluster+'_'+fold, 'a+') as outf:
                for line in lines[(index*2):(index*2)+2]:
                    outf.write(line)

def setup_pool(workers=50):
    pool_inputs = []
    for cluster in range(1,25):
        for fold in range(10):
            if os.path.exists('/mnt/lab_data3/soumyak/adpd/nn_analysis/input/effect/'+str(cluster)+'_'+str(fold)):
                effect_in = '/mnt/lab_data3/soumyak/adpd/nn_analysis/input/effect/'+str(cluster)+'_'+str(fold)
                effect_out = '/mnt/lab_data3/soumyak/adpd/nn_analysis/output/effect/'+str(cluster)+'_'+str(fold)
                noneffect_in = '/mnt/lab_data3/soumyak/adpd/nn_analysis/input/noneffect/'+str(cluster)+'_'+str(fold)
                noneffect_out = '/mnt/lab_data3/soumyak/adpd/nn_analysis/output/noneffect/'+str(cluster)+'_'+str(fold)
                model = '/mnt/lab_data3/soumyak/adpd/clusters_gkmsvm/Cluster'+str(cluster)+'/fold'+str(fold)+'/train/train.output.model.txt'
                pool_inputs.append((effect_in, model, effect_out))
                pool_inputs.append((noneffect_in, model, noneffect_out))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        merge=pool.map(run_explain, pool_inputs)

def run_explain(inputs):
    os.system('/users/soumyak/lsgkm/src/gkmexplain ' + inputs[0] + ' ' + inputs[1] + ' ' + inputs[2])

def concat():
    effect_catted = []
    noneffect_catted = []
    for cluster in range(1,25):
        for fold in range(10):
            if os.path.exists('/mnt/lab_data3/soumyak/adpd/nn_analysis/output/effect/'+str(cluster)+'_'+str(fold)):
                with open('/mnt/lab_data3/soumyak/adpd/nn_analysis/output/effect/'+str(cluster)+'_'+str(fold)) as inf:
                    lines = inf.readlines()
                    effect_catted += lines
                with open('/mnt/lab_data3/soumyak/adpd/nn_analysis/output/noneffect/'+str(cluster)+'_'+str(fold)) as inf:
                    lines = inf.readlines()
                    noneffect_catted += lines
    return effect_catted, noneffect_catted

def to_file(effect, noneffect):
    with open('/mnt/lab_data3/soumyak/adpd/nn_analysis/nn.effect.scores.txt', 'w') as outf:
        for line in effect:
            outf.write(line)
    with open('/mnt/lab_data3/soumyak/adpd/nn_analysis/nn.noneffect.scores.txt', 'w') as outf:
        for line in noneffect:
            outf.write(line)


if __name__ == "__main__":
    workers = sys.argv[1]
    main([workers])
