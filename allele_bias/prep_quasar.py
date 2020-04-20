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
        if not os.path.isdir('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allele_bias/quasar/input/' + pat):
            os.mkdir('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allele_bias/quasar/input/' + pat)
        with open('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allele_bias/quasar/bam_lists/' + pat + '_ctrl_bams.txt', 'w') as outfile:
            for bam in patient_bams:
                outfile.write(bam)

for pat in multi_bam_pats:
    print(pat)
    with open('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allele_bias/quasar/bam_lists/' + pat + '_ctrl_bams.txt') as infile:
        pat_bams = [i.strip() for i in infile.readlines()]
        for bam in pat_bams:
            bam_name = bam.split('/')[10]
            mpileup_cmd = 'sbatch --export=ALL -n 1 -t 1-0 -p akundaje --mail-type=ALL -o output/' + bam_name + '.o -e output/' + bam_name + '.e -J ' + bam_name + ' run_mpileup.sh ' + bam + ' ' + bam_name
            mpileup_cmd = mpileup_cmd.split()
            print(mpileup_cmd)
            ret = subprocess.call(mpileup_cmd)

            #format_cmd = "zcat /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allele_bias/quasar/pileup/" + bam_name + ".pileup.gz | awk -v OFS='\t' '{ if ($4>0 && $5 !~ /[^\^][<>]/ && $5 !~ /\+[0-9]+[ACGTNacgtn]+/ && $5 !~ /-[0-9]+[ACGTNacgtn]+/ && $5 !~ /[^\^]\*/) print $1,$2-1,$2,$3,$4,$5,$6}' | sortBed -i stdin | intersectBed -a stdin -b /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allele_bias/snps/hg38_1KG_ADPD_snps.bed -wo | cut -f 1-7,11-14 | gzip > /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allele_bias/quasar/pileup_beds/" + bam_name + ".pileup.bed.gz"
            #print(format_cmd)
            #print("FORMAT")
            #format_cmd = format_cmd.split()
            #ret = subprocess.call(format_cmd)
            #r_cmd = "R --vanilla --args /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/allele_bias/quasar/pileup_beds/" + bam_name + ".pileup.bed.gz < /users/soumyak/QuASAR/scripts/convertPileupToQuasar.R"
            #print(r_cmd)
            #print("R")
            #r_cmd = r_cmd.split()
            #ret = r_cmd.split()
