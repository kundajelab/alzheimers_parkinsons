import os
import subprocess
import pandas as pd


metadata = pd.read_excel('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/190215_Brain-ControlsOnly_Metadata_Merged.xlsx')
patients = list(metadata['PatientID'].unique())

with open('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/ctrl_bams.txt') as infile:
    ctrl_bams = infile.readlines()

multi_bam_pats = []
for pat in patients:
    print(pat)
    patient_bams = []
    for bam in ctrl_bams:
        if pat in bam:
            patient_bams.append(bam)
    if len(patient_bams) > 1:
        multi_bam_pats.append(pat)
        patient_bams.sort()
        if not os.path.isdir('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allelic_imbalance/quasar/input/' + pat):
            os.mkdir('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allelic_imbalance/quasar/input/' + pat)
        if not os.path.isdir('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allelic_imbalance/quasar/output/' + pat):
            os.mkdir('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allelic_imbalance/quasar/output/' + pat)
        if not os.path.isfile('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allelic_imbalance/quasar/bam_lists/' + pat + '_ctrl_bams.txt'):
            with open('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allelic_imbalance/quasar/bam_lists/' + pat + '_ctrl_bams.txt', 'w') as outfile:
                for bam in patient_bams:
                    outfile.write(bam)

for pat in multi_bam_pats:
    print(pat)
    with open('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allelic_imbalance/quasar/bam_lists/' + pat + '_ctrl_bams.txt') as infile:
        pat_bams = [i.strip() for i in infile.readlines()]
        for bam in pat_bams:
            bam_name = bam.split('/')[10]
            #mpileup_cmd = 'sbatch --export=ALL -n 1 -t 10:00 -p akundaje -o output/' + bam_name + '.o -e output/' + bam_name + '.e -J ' + bam_name + ' run_mpileup.sh ' + bam + ' ' + bam_name
            #mpileup_cmd = mpileup_cmd.split()
            #print(mpileup_cmd)
            #ret = subprocess.call(mpileup_cmd)

            #format_cmd = 'sbatch --export=ALL -n 1 -t 10:00 -p akundaje -o output/' + bam_name + '.o -e output/' + bam_name + '.e -J ' + bam_name + ' run_format.sh ' + bam_name
            #format_cmd = format_cmd.split()
            #print(format_cmd)
            #ret = subprocess.call(format_cmd)

            r_cmd = 'sbatch --export=ALL -n 1 -t 10:00 -p akundaje -o output/' + bam_name + '.o -e output/' + bam_name + '.e -J ' + bam_name + ' run_R.sh ' + bam_name
            r_cmd = r_cmd.split()
            print(r_cmd)
            ret = subprocess.call(r_cmd)

