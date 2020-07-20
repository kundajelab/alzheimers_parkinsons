import pandas as pd
import sys

clust_to_celltype = {1: 'excitatory neurons',
                     2: 'inhibitory neurons',
                     3: 'excitatory neurons',
                     4: 'excitatory neurons',
                     5: 'nigral neurons',
                     6: 'nigral neurons',
                     7: 'unknown neurons',
                     8: 'opcs',
                     9: 'opcs',
                     10: 'opcs',
                     11: 'inhibitory neurons',
                     12: 'inhibitory neurons',
                     13: 'astrocytes',
                     14: 'astrocytes',
                     15: 'astrocytes',
                     16: 'astrocytes',
                     17: 'astrocytes',
                     18: 'doublets',
                     19: 'oligodendrocytes',
                     20: 'oligodendrocytes',
                     21: 'oligodendrocytes',
                     22: 'oligodendrocytes',
                     23: 'oligodendrocytes',
                     24: 'microglia'}

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
        clust_name = clust_to_celltype[cluster]
        cluster = str(cluster)
        outfile.write('[cluster'+cluster+']\n')
        outfile.write('\n')
        outfile.write('file = /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/croo_outputs/Cluster'+cluster+'/signal/rep1/Cluster'+cluster+'.fc.signal.bigwig\n')
        outfile.write('height = 4\n')
        outfile.write('title = Cluster '+cluster+' - ' + clust_name + '\n')
        outfile.write('min_value = 0\n')
        outfile.write('max_value = 25\n')
        outfile.write('\n')
        outfile.write('[spacer]\n')
        outfile.write('\n')

def write_pval_bw(outfile):
    for cluster in range(1, 25):
        clust_name = clust_to_celltype[cluster]
        cluster = str(cluster)
        outfile.write('[cluster'+cluster+']\n')
        outfile.write('\n')
        outfile.write('file = /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/croo_outputs/Cluster'+cluster+'/signal/rep1/Cluster'+cluster+'.pval.signal.bigwig\n')
        outfile.write('height = 4\n')
        outfile.write('title = Cluster '+cluster+' - ' + clust_name + '\n')
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
