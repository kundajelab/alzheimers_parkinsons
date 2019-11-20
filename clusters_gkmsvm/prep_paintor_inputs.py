import pandas as pd
import sys
import os


def main(args):
    snps = pd.read_csv('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/snps_final/final_kunkle_with_zcores.tsv',
                     sep='\t')
    loci = snps.locus_num.unique()
    for i in loci:
        file_addr = '/mnt/lab_data3/soumyak/adpd/paintor/data/locus'+str(i)+'.hdl'
        locus_df = prep_locus(snps, i, file_addr)
        get_ld(locus_df, file_addr)

def prep_locus(snps, locus, file_addr):
    locus_df = snps.loc[snps['locus_num'] == locus]
    locus_df = locus_df[['chr', 'pos', 'rsid', 'effect_allele', 'non_effect_allele', 'zscore']]
    locus_df.to_csv(file_addr, sep='\t', index=False)
    return locus_df

def get_ld(locus_df, file_addr):
    assert len(locus_df.chr.unique()) == 1
    chrom = locus_df.chr.unique()[0]
    os.system('python /users/soumyak/PAINTOR_V3.0/PAINTOR_Utilities/CalcLD_1KG_VCF.py '
              + '--locus ' + file_addr + ' '
              + '--reference ' + *******REF********
              + '--map ' + *********MAP**********
              + '--effect_allele effect_allele '
              + '--alt_allele non_effect_allele '
              + '--population EUR '
              + '--Zhead zscore '
              + '--out_name /mnt/lab_data3/soumyak/adpd/paintor/data/locus'+str(i)+'.ld '
              + '--position pos')

if __name__ == "__main__":
    main(sys.argv[1:])
