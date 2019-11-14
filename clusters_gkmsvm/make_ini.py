import pandas as pd
import sys


def main(args):
    make_ini()

def make_ini():
    with open('/mnt/lab_data3/soumyak/adpd/pytracks/fc_bigwig_snps.ini', 'w') as outfile:
        write_fc_bw(outfile)
        write_snps_peaks_vlines(outfile)
    with open('/mnt/lab_data3/soumyak/adpd/pytracks/pval_bigwig_snps.ini', 'w') as outfile:
        write_pval_bw(outfile)
        write_snps_peaks_vlines(outfile)

def write_fc_bw(outfile):
    for cluster in range(1, 25):
        cluster = str(cluster)
        outfile.write('[cluster'+cluster+']\n')
        outfile.write('\n')
        outfile.write('file = /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/croo_outputs/Cluster'+cluster+'/signal/rep1/Cluster'+cluster+'.fc.signal.bigwig\n')
        outfile.write('height = 4\n')
        outfile.write('title = Cluster '+cluster+'\n')
        outfile.write('min_value = 0\n')
        outfile.write('max_value = 25\n')
        outfile.write('\n')
        outfile.write('[spacer]\n')
        outfile.write('\n')

def write_pval_bw(outfile):
    for cluster in range(1, 25):
        cluster = str(cluster)
        outfile.write('[cluster'+cluster+']\n')
        outfile.write('\n')
        outfile.write('file = /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/croo_outputs/Cluster'+cluster+'/signal/rep1/Cluster'+cluster+'.pval.signal.bigwig\n')
        outfile.write('height = 4\n')
        outfile.write('title = Cluster '+cluster+'\n')
        outfile.write('min_value = 0\n')
        outfile.write('max_value = 25\n')
        outfile.write('\n')
        outfile.write('[spacer]\n')
        outfile.write('\n')

def write_snps_peaks_vlines(outfile):
    outfile.write('[snps]\n')
    outfile.write('file = /mnt/lab_data3/soumyak/adpd/sig_snps/all.sig.snps.bed\n')
    outfile.write('height = 4\n')
    outfile.write('title = SNPs\n')
    outfile.write('file_type = bed\n')
    outfile.write('\n')
    #outfile.write('[genes]\n')
    #outfile.write('file = /mnt/lab_data3/soumyak/adpd/new.overlap.bed\n')
    #outfile.write('height = 4\n')
    #outfile.write('title = Overlap Peaks\n')
    #outfile.write('file_type = bed\n')
    #outfile.write('\n')
    outfile.write('[spacer]\n')
    outfile.write('\n')
    outfile.write('[x-axis]\n')
    outfile.write('\n')
    outfile.write('[vlines]\n')
    outfile.write('\n')
    outfile.write('file = /mnt/lab_data3/soumyak/adpd/sig_snps/all.sig.snps.bed\n')
    outfile.write('type = vlines\n')


if __name__ == '__main__':
    main(sys.argv[1:])
