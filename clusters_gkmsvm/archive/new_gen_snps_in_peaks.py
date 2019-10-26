import sys
import pandas as pd
import pybedtools
import tabix
import pysam


gwas_to_file = {'Kunkle': '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mgloud_GWAS_HG19/GWAS_Kunkle2019.txt.gz',
                '23andme_PD': '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mgloud_GWAS_HG19/23andme_PD.txt.gz',
                'Jansen': '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mgloud_GWAS_HG19/GWAS_Alzheimers_Jansen_2018.txt.gz',
                'Lambert': '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mgloud_GWAS_HG19/GWAS_Alzheimers_Lambert_2013.txt.gz',
                'Pankratz': '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/mgloud_GWAS_HG19/GWAS_Parkinsons_Pankratz_2012.txt.gz'}

ld_file = '/mnt/lab_data/kundaje/users/pgreens/LD/EUR_geno.txt.gz'
ld_data = tabix.open(ld_file)
dbsnp_file = '/mnt/lab_data3/soumyak/refs/hg19/dbSNP/00-All.vcf.gz'
dbsnp = tabix.open(dbsnp_file)
ref_fasta = '/mnt/lab_data3/soumyak/refs/hg19/male.hg19.fa'
ref_gen = pysam.FastaFile(ref_fasta)

def main(args):
    for gwas_name in ['Kunkle']:
        print("GWAS: ", gwas_name)
        gwas = read_gwas(gwas_to_file[gwas_name])
        gwas = prep_gwas(gwas)
        #ld_df = ld_expand(gwas, ld_file)
        #gwas_in_peaks(gwas_name, ld_df)


def read_gwas(gwas_file):
    print("Reading GWAS File")
    gwas = pd.read_csv(gwas_file, sep='\t')
    return gwas


def prep_gwas(gwas):
    print("Preparing GWAS File")
    gwas['pvalue'] = gwas['pvalue'].astype('float')
    gwas = gwas.loc[gwas['pvalue'] < 5e-08]
    gwas.rename(columns = {'snp_pos':'end', 'ref':'non_effect', 'alt':'effect', 'non_effect_allele':'non_effect', 'effect_allele':'effect'}, inplace=True)
    gwas['start'] = gwas['end'] - 1
    gwas = gwas[['chr', 'start', 'end', 'rsid', 'pvalue', 'non_effect', 'effect']]
    gwas['chr'] = gwas['chr'].apply(lambda x: 'chr' + str(x).strip('chr'))
    gwas.sort_values(by=['chr', 'start'], inplace=True)
    print(len(gwas))
    return gwas


def ld_expand(gwas, ld_file):
    print("Expanding GWAS SNPs")
    ld_dict = {'ld_chr': [], 'ld_start': [], 'ld_end': [], 'ld_rsid': [],'ld_val': [],
                  'chr': [], 'start': [], 'end': [], 'rsid': [], 'pvalue': [],
                  'non_effect': [], 'effect': [], 'ref': [], 'alt': [], 'major': [], 'minor': []}
    counter = 0
    for index,row in gwas.iterrows():
        counter += 1
        if counter % 100 == 0:
            print(counter)
        chrom = row['chr']
        start = row['start']
        end = row['end']
        rsid = row['rsid']
        pvalue = row['pvalue']
        non_effect = row['non_effect']
        effect = row['effect']
        matches = dbsnp.query(chrom.strip('chr'), start, end)
        gotmatches = False
        for match in matches:
            if match[2] == rsid:
                ref = match[3]
                if ',' in match[4]:
                    alleles = [match[3]] + match[4].split(',')
                    alt = match[4].split(',')
                else:
                    alleles = [match[3], match[4]]
                    alt = [match[4]]
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
                minors = alleles
                minors.remove(major)
            elif 'TOPMED' in match[7]:
                topmed_freqs = match[7].split('TOPMED=')[1].split(',')
                topmed_max_freq = max(topmed_freqs)
                topmed_max_ind = topmed_freqs.index(topmed_max_freq)
                major = alleles[topmed_max_ind]
                minors = alleles
                minors.remove(major)
            elif 'CAF' in match[7]:
                caf_freqs = match[7].split('CAF=')[1].split(';')[0].split(',')
                caf_max_freq = max(caf_freqs)
                caf_max_ind = caf_freqs.index(caf_max_freq)
                major = alleles[caf_max_ind]
                minors = alleles
                minors.remove(major)
            else:
                major = alleles[0]
                minors = alleles
                minors.remove(major)
            for ind,minor in enumerate(minors):
                ld_dict['ld_chr'].append(chrom)
                ld_dict['ld_start'].append(start)
                ld_dict['ld_end'].append(end)
                ld_dict['ld_rsid'].append(rsid)
                ld_dict['ld_val'].append(1)
                ld_dict['chr'].append(chrom)
                ld_dict['start'].append(start)
                ld_dict['end'].append(end)
                ld_dict['rsid'].append(rsid)
                ld_dict['pvalue'].append(pvalue)
                ld_dict['non_effect'].append(non_effect)
                ld_dict['effect'].append(effect)
                ld_dict['ref'].append(ref)
                ld_dict['alt'].append(alt[ind])
                ld_dict['major'].append(major)
                ld_dict['minor'].append(minor)
        else:
            ld_dict['ld_chr'].append(chrom)
            ld_dict['ld_start'].append(start)
            ld_dict['ld_end'].append(end)
            ld_dict['ld_rsid'].append(rsid)
            ld_dict['ld_val'].append(1)
            ld_dict['chr'].append(chrom)
            ld_dict['start'].append(start)
            ld_dict['end'].append(end)
            ld_dict['rsid'].append(rsid)
            ld_dict['pvalue'].append(pvalue)
            ld_dict['non_effect'].append(non_effect)
            ld_dict['effect'].append(effect)
            ld_dict['ref'].append(non_effect)
            ld_dict['alt'].append(effect)
            ld_dict['major'].append(non_effect)
            ld_dict['minor'].append(effect)
        ld_snps = ld_data.query(chrom, start, end)
        ld_snps = [i for i in ld_snps]
        for index,row in enumerate(ld_snps):
            matches = dbsnp.query(row[4].strip('chr'), int(row[5]), int(row[6]))
            gotmatches = False
            for match in matches:
                if match[2] == row[7]:
                    ref = match[3]
                    if ',' in match[4]:
                        alleles = [match[3]] + match[4].split(',')
                        alt = match[4].split(',')
                    else:
                        alleles = [match[3], match[4]]
                        alt = [match[4]]
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
                    minors = alleles
                    minors.remove(major)
                elif 'TOPMED' in match[7]:
                    topmed_freqs = match[7].split('TOPMED=')[1].split(',')
                    topmed_max_freq = max(topmed_freqs)
                    topmed_max_ind = topmed_freqs.index(topmed_max_freq)
                    major = alleles[topmed_max_ind]
                    minors = alleles
                    minors.remove(major)
                elif 'CAF' in match[7]:
                    caf_freqs = match[7].split('CAF=')[1].split(';')[0].split(',')
                    caf_max_freq = max(caf_freqs)
                    caf_max_ind = caf_freqs.index(caf_max_freq)
                    major = alleles[caf_max_ind]
                    minors = alleles
                    minors.remove(major)
                else:
                    major = alleles[0]
                    minors = alleles
                    minors.remove(major)
                for ind,minor in enumerate(minors):
                    ld_dict['ld_chr'].append(row[4])
                    ld_dict['ld_start'].append(int(row[5]))
                    ld_dict['ld_end'].append(int(row[6]))
                    ld_dict['ld_rsid'].append(row[7])
                    ld_dict['ld_val'].append(float(row[8]))
                    ld_dict['chr'].append(row[0])
                    ld_dict['start'].append(int(row[1]))
                    ld_dict['end'].append(int(row[2]))
                    ld_dict['rsid'].append(rsid)
                    ld_dict['pvalue'].append(pvalue)
                    ld_dict['non_effect'].append(non_effect)
                    ld_dict['effect'].append(effect)
                    ld_dict['ref'].append(ref)
                    ld_dict['alt'].append(alt[ind])
                    ld_dict['major'].append(major)
                    ld_dict['minor'].append(minor)
            else:
                ref = ref_gen.fetch(row[4], int(row[5]), int(row[6]))
                ref = ref.upper()
                assert len(ref) == 1
                alts = ['A', 'T', 'C', 'G']
                alts.remove(ref)
                assert len(alts) == 3
                for a in alts:
                    ld_dict['ld_chr'].append(row[4])
                    ld_dict['ld_start'].append(int(row[5]))
                    ld_dict['ld_end'].append(int(row[6]))
                    ld_dict['ld_rsid'].append(row[7])
                    ld_dict['ld_val'].append(float(row[8]))
                    ld_dict['chr'].append(row[0])
                    ld_dict['start'].append(int(row[1]))
                    ld_dict['end'].append(int(row[2]))
                    ld_dict['rsid'].append(rsid)
                    ld_dict['pvalue'].append(pvalue)
                    ld_dict['non_effect'].append(non_effect)
                    ld_dict['effect'].append(effect)
                    ld_dict['ref'].append(ref)
                    ld_dict['alt'].append(a)
                    ld_dict['major'].append(ref)
                    ld_dict['minor'].append(a)
    ld_df = pd.DataFrame.from_dict(ld_dict)
    ld_df.sort_values(by=['ld_chr', 'ld_start', 'ld_end', 'ld_rsid', 'ld_val', 'minor'], inplace=True)
    ld_df.drop_duplicates(subset=['ld_chr', 'ld_start', 'ld_end', 'ld_rsid', 'minor'], inplace=True)
    return ld_df


def gwas_in_peaks(name, ld_df):
    print("Intersecting SNPs with Peaks")
    gwas_bed = pybedtools.BedTool.from_dataframe(ld_df)
    for i in range(1, 25):
        print("Cluster ", str(i))
        overlap_peaks = '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs/peaks/hg19_overlap_peaks_bedtools_merged/Cluster'+str(i)+'.overlap.optimal.narrowPeak'
        peak_bed = pybedtools.BedTool(overlap_peaks)
        intersect_bed = gwas_bed.intersect(peak_bed, u=True, wa=True)
        intersect_df = pybedtools.BedTool.to_dataframe(intersect_bed)
        intersect_df.columns = ['ld_chr', 'ld_start', 'ld_end', 'ld_rsid','ld_val', 'chr', 'start', 'end', 'rsid', 'pvalue', 'non_effect', 'effect', 'ref', 'alt', 'major', 'minor']
        intersect_df.sort_values(by=['ld_chr', 'ld_start', 'ld_end', 'ld_rsid', 'ld_val', 'minor'], inplace=True)
        intersect_df.drop_duplicates(subset=['ld_chr', 'ld_start', 'ld_end', 'ld_rsid', 'minor'], inplace=True)
        intersect_df.to_csv('/mnt/lab_data3/soumyak/adpd/snp_lists/'+name+'/expanded/Cluster'+str(i)+'.overlap.expanded.snps.hg19.bed', sep='\t', index=False)


if __name__ == '__main__':
    main(sys.argv[1:])
