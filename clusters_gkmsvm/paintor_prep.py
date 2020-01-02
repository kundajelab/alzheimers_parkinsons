import pandas as pd
import sys
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import pybedtools


def main(args):
    adpd_snps = pd.read_csv('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/snps_final/191121_ld_buddies_table_stage3.tsv',
                     sep='\t')
    kunkle_snps = pd.read_csv('/mnt/lab_data3/soumyak/adpd/gwas/GWAS_Kunkle2019.txt',
                              sep='\t')
    #paintor_snps = get_snps(adpd_snps, kunkle_snps)
    paintor_snps = pd.read_csv('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/snps_final/final_kunkle_with_zcores.tsv',
                               sep='\t')
    loci = paintor_snps.locus_num.unique()
    ld_pool = []
    annot_pool = []
    for i in loci:
        if int(i) != 71 and int(i) != 113:
            file_addr = '/mnt/lab_data3/soumyak/adpd/paintor/data/locus'+str(i)
            prep_locus(paintor_snps, i, file_addr)
            ld_pool.append((file_addr, i))
            annot_pool.append((file_addr, i))
    with ProcessPoolExecutor(max_workers = int(args[0])) as pool:
        merge = pool.map(get_ld, ld_pool)
    with ProcessPoolExecutor(max_workers = int(args[0])) as pool:
        merge = pool.map(get_annot, annot_pool)
    os.system('cd /mnt/lab_data3/soumyak/adpd/paintor/data/; ls locus*.processed > input.files')
    #os.system('/users/soumyak/PAINTOR_V3.0/PAINTOR -input /mnt/lab_data3/soumyak/adpd/paintor/data/input.files -in /mnt/lab_data3/soumyak/adpd/paintor/data -out /mnt/lab_data3/soumyak/adpd/paintor/data -Zhead zscore -LDname ld -enumerate 1 -annotations atac,cds')
    #os.system('/users/soumyak/PAINTOR_V3.0/PAINTOR -input /mnt/lab_data3/soumyak/adpd/paintor/data/input.files -in /mnt/lab_data3/soumyak/adpd/paintor/data -out /mnt/lab_data3/soumyak/adpd/paintor/data -Zhead zscore -LDname ld -enumerate 1 -annotations atac')
    os.system('/users/soumyak/PAINTOR_V3.0/PAINTOR -input /mnt/lab_data3/soumyak/adpd/paintor/data/input.files -in /mnt/lab_data3/soumyak/adpd/paintor/data -out /mnt/lab_data3/soumyak/adpd/paintor/data -Zhead zscore -LDname ld -enumerate 1')
    for i in loci:
        if int(i) != 71 and int(i) != 113:
            print("Locus ", str(i))
            os.system('sort -k7,7gr /mnt/lab_data3/soumyak/adpd/paintor/data/locus'+str(i)+'.processed.results | grep -v rsid > /mnt/lab_data3/soumyak/adpd/paintor/data/locus'+str(i)+'.processed.sortedresults')
            results = pd.read_csv('/mnt/lab_data3/soumyak/adpd/paintor/data/locus'+str(i)+'.processed.sortedresults', sep=' ', header=None)
            results.drop(columns=[5,6], inplace=True)
            results.to_csv('/mnt/lab_data3/soumyak/adpd/paintor/data/locus'+str(i)+'.processed.onlysnps', sep=' ', header=False, index=False)

def get_snps(adpd_snps, kunkle_snps):
    loci = adpd_snps[['chr', 'rsid', 'locus_num']]
    trimmed_kunkle = kunkle_snps.drop(columns=['chr', 'pvalue', 'effect_direction', 'MarkerName'])
    joined = loci.merge(trimmed_kunkle, on='rsid')
    joined['chr'] = joined['chr'].apply(lambda x : 'chr' + str(x))
    joined.sort_values(by=['locus_num', 'chr', 'snp_pos', 'rsid'], inplace=True)
    joined.drop_duplicates(subset=['rsid', 'snp_pos'], inplace=True)
    joined['zscore'] = joined['beta'] / joined['se']
    joined = joined[['chr', 'snp_pos', 'rsid', 'locus_num', 'effect_allele', 'non_effect_allele', 'beta', 'se', 'zscore']]
    joined.to_csv('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/snps_final/final_kunkle_with_zcores.tsv',
                  sep='\t', index=False)
    return joined

def prep_locus(snps, locus, file_addr):
    locus_df = snps.loc[snps['locus_num'] == locus]
    locus_df = locus_df[['chr', 'snp_pos', 'rsid', 'effect_allele', 'non_effect_allele', 'zscore']]
    locus_df.to_csv(file_addr, sep='\t', index=False)

def get_ld(inputs):
    locus_df = pd.read_csv(inputs[0], sep='\t')
    assert len(locus_df.chr.unique()) == 1
    chrom = locus_df.chr.unique()[0]
    print("Locus ", inputs[1])
    os.system('python /users/soumyak/PAINTOR_V3.0/PAINTOR_Utilities/CalcLD_1KG_VCF.py '
              + '--locus ' + inputs[0] + ' '
              + '--reference /mnt/lab_data3/soumyak/refs/1KG/ALL.'
              + chrom + '.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz '
              + '--map /mnt/lab_data3/soumyak/refs/1KG/integrated_call_samples_v3.20130502.ALL.panel '
              + '--effect_allele effect_allele '
              + '--alt_allele non_effect_allele '
              + '--population EUR '
              + '--Zhead zscore '
              + '--out_name ' + inputs[0] + ' '
              + '--drop_mono False '
              + '--position snp_pos')
    os.system('mv ' + inputs[0] + '.ld ' + inputs[0] + '.processed.ld')

def get_annot(inputs):
    print("Locus ", inputs[1])
    #os.system('python /users/soumyak/PAINTOR_V3.0/PAINTOR_Utilities/AnnotateLocus.py '
    #          + '--input /mnt/lab_data3/soumyak/adpd/paintor/annotation_paths '
    #          + '--locus ' + inputs[0] + ' '
    #          + '--out ' + inputs[0] + '.processed.annotations '
    #          + '--chr chr '
    #          + '--pos snp_pos')
    locus = pd.read_csv(inputs[0], sep='\t', header=None)
    locus = locus.iloc[1:,:]
    locus[1] = locus[1].astype(int)
    locus[6] = locus[1] - 1
    locus = locus[[0,6,1,2]]
    bed = pybedtools.BedTool.from_dataframe(locus)
    intersect_atac = bed.intersect('/mnt/lab_data3/soumyak/adpd/paintor/atac', c=True)
    intersect_cds = bed.intersect('/mnt/lab_data3/soumyak/adpd/paintor/cds', c=True)
    locus_atac = intersect_atac.to_dataframe()
    locus_cds = intersect_cds.to_dataframe()
    locus_atac['atac'] = locus_atac['score'].apply(lambda x: x if x == 0 else 1)
    locus_atac['cds'] = locus_cds['score'].apply(lambda x: x if x == 0 else 1)
    locus_atac[['atac','cds']].to_csv('/mnt/lab_data3/soumyak/adpd/paintor/data/locus'+str(inputs[1])+'.processed.annotations', index=False, header=True, sep=' ')


if __name__ == "__main__":
    main(sys.argv[1:])
