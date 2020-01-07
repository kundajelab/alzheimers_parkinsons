import pandas as pd

bigwigs = pd.read_csv('/users/soumyak/alzheimers_parkinsons/model_inputs/sc.fc.bigwig', sep='\t', header=None)
idr_peaks = pd.read_csv('/users/soumyak/alzheimers_parkinsons/model_inputs/sc.idr.peaks', sep='\t', header=None)
ambig_peaks = pd.read_csv('/users/soumyak/alzheimers_parkinsons/model_inputs/sc.ambig.peaks', sep='\t', header=None)
sc_tasks = '/users/soumyak/alzheimers_parkinsons/model_inputs/sc.tasks.tsv'
task_dict=dict()

for index,row in idr_peaks.iterrows():
    task = row[1]
    task_dict[task] = [row[0]]

for index,row in bigwigs.iterrows():
    task = row[1]
    task_dict[task].append(row[0])

for index,row in ambig_peaks.iterrows():
    task = row[1]
    task_dict[task].append(row[0])

outf=open(sc_tasks,'w')
for task in task_dict:
    outf.write(task+'\t'+'\t'.join(task_dict[task])+'\n')
