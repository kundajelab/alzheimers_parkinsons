import pandas as pd

basedir_oak = '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/' \
              + 'pseudobulk/pseudobulk_outputs/croo_outputs/'
basedir_mnt = '/mnt/lab_data3/soumyak/adpd/'

sc_tasks = 'single-cell_inputs/sc.tasks.tsv'
task_dict = {}

for task in range(1,25):
    task = 'Cluster' + str(task)
    idr_peaks = basedir_mnt + 'idr_peaks/' + task + '.idr.optimal.narrowPeak'
    bigwigs = basedir_oak + task + '/signal/rep1/' + task + '.fc.signal.bigwig'
    ambig_peaks = basedir_mnt + 'ambiguous/' + task + '.ambiguous.bed'
    task_dict[task] = [idr_peaks, bigwigs, ambig_peaks]

outf = open(sc_tasks, 'w')
for task in task_dict:
    outf.write(task + '\t' + '\t'.join(task_dict[task]) + '\n')

