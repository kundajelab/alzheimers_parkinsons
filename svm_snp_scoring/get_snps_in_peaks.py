import sys
import pandas as pd
import pybedtools
import tabix
import pysam

snp_file = '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/snps_final/ld_buddies_table_stage2_2019-10-25.tsv'
dbsnp_file = '/oak/stanford/groups/akundaje/refs/hg38/dbSNP/00-All.vcf.gz'
dbsnp = tabix.open(dbsnp_file)


def main(args):
    print("Reading SNP File")
    snps = pd.read_csv(snp_file, sep='\t')
    snps = prep_snps(snps)
    snps = get_alleles(snps)
    snps_in_peaks(snps)


def prep_snps(snps):
    print("Preparing SNP File")
    snps.rename(columns = {'pos': 'end', 'effect_allele': 'effect', 'noneffect_allele': 'noneffect'}, inplace=True)
    snps['chr'] = snps['chr'].apply(lambda x: 'chr' + str(x).strip('chr'))
    snps['chr'] = snps['chr'].astype(str)
    snps['start'] = snps['end'] - 1
    snps['start'] = snps['start'].astype(int)
    snps['end'] = snps['end'].astype(int)
    snps['effect'] = snps['effect'].apply(lambda x: str(x).upper())
    snps['noneffect'] = snps['noneffect'].apply(lambda x: str(x).upper())
    snps = snps[['chr', 'start', 'end', 'rsid', 'effect', 'noneffect', 'direction', 'pvalue', 'source_gwas', 'locus_num', 'ld_tag_chr', 'ld_tag_pos', 'r2_with_ld_tag']]
    snps.sort_values(by=['chr', 'start', 'end', 'rsid', 'effect', 'noneffect'], inplace=True)
    return snps


def get_alleles(snps):
    print("Getting dbSNP Alleles")
    ref_list = []
    alt_list = []
    major_list = []
    minor_list = []
    counter = 0
    for index,row in snps.iterrows():
        counter += 1
        if counter % 100 == 0:
            print(counter)
        chrom = row['chr']
        start = row['start']
        end = row['end']
        rsid = row['rsid']
        effect = row['effect']
        noneffect = row['noneffect']
        matches = dbsnp.query(chrom.strip('chr'), start, end)
        gotmatches = False
        for match in matches:
            if match[2] == rsid:
                ref = match[3]
                if ',' in match[4]:
                    alleles = [match[3]] + match[4].split(',')
                    alt = match[4]
                else:
                    alleles = [match[3], match[4]]
                    alt = match[4]
                gotmatches = True
                break
        if gotmatches:
            if 'TOPMED' in match[7] and 'CAF' in match[7]:
                topmed_freqs = match[7].split('TOPMED=')[1].split(',')
                topmed_max_freq = max(topmed_freqs)
                topmed_max_ind = topmed_freqs.index(topmed_max_freq)
                caf_freqs = match[7].split('CAF=')[1].split(';')[0].split(',')
                caf_max_freq = max(caf_freqs)
                caf_max_ind = caf_freqs.index(caf_max_freq)
                major = alleles[topmed_max_ind]
                minor = alleles
                minor.remove(major)
            elif 'TOPMED' in match[7]:
                topmed_freqs = match[7].split('TOPMED=')[1].split(',')
                topmed_max_freq = max(topmed_freqs)
                topmed_max_ind = topmed_freqs.index(topmed_max_freq)
                major = alleles[topmed_max_ind]
                minor = alleles
                minor.remove(major)
            elif 'CAF' in match[7]:
                caf_freqs = match[7].split('CAF=')[1].split(';')[0].split(',')
                caf_max_freq = max(caf_freqs)
                caf_max_ind = caf_freqs.index(caf_max_freq)
                major = alleles[caf_max_ind]
                minor = alleles
                minor.remove(major)
            else:
                major = '.'
                minor = ['.']
            minor = ','.join(minor)
        else:
            ref = '.'
            alt = '.'
            major = '.'
            minor = '.'
        ref_list.append(ref)
        alt_list.append(alt)
        major_list.append(major)
        minor_list.append(minor)
    snps['ref'] = ref_list
    snps['alt'] = alt_list
    snps['major'] = major_list
    snps['minor'] = minor_list
    snps = snps[['chr', 'start', 'end', 'rsid', 'effect', 'noneffect', 'ref', 'alt', 'major', 'minor', 'direction', 'pvalue', 'source_gwas', 'locus_num', 'ld_tag_chr', 'ld_tag_pos', 'r2_with_ld_tag']]
    snps.sort_values(by=['chr', 'start', 'end', 'rsid', 'effect', 'noneffect'], inplace=True)
    snps.drop_duplicates(subset=['chr', 'start', 'end', 'rsid', 'effect', 'noneffect'], inplace=True)
    return snps


def snps_in_peaks(snps):
    print("Intersecting SNPs with Peaks")
    snps_bed = pybedtools.BedTool.from_dataframe(snps)
    for i in range(1, 25):
        print("Cluster ", str(i))
        overlap_peaks = '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/overlap_peaks_bedtools_merged/Cluster'+str(i)+'.overlap.optimal.narrowPeak'
        peak_bed = pybedtools.BedTool(overlap_peaks)
        intersect_bed = snps_bed.intersect(peak_bed, u=True, wa=True)
        intersect_df = pybedtools.BedTool.to_dataframe(intersect_bed, header=None)
        intersect_df.columns = ['chr', 'start', 'end', 'rsid', 'effect', 'noneffect', 'ref', 'alt', 'major', 'minor', 'direction', 'pvalue', 'source_gwas', 'locus_num', 'ld_tag_chr', 'ld_tag_pos', 'r2_with_ld_tag']
        intersect_df.sort_values(by=['chr', 'start', 'end', 'rsid', 'effect', 'noneffect'], inplace=True)
        intersect_df.drop_duplicates(subset=['chr', 'start', 'end', 'rsid', 'effect', 'noneffect'], inplace=True)
        intersect_df.to_csv('/mnt/lab_data3/soumyak/adpd/snp_lists/Cluster'+str(i)+'.overlap.expanded.snps.hg38.bed', sep='\t', index=False)


if __name__ == '__main__':
    main(sys.argv[1:])
