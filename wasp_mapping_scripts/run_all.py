# this python script runs the entire pipeline
import subprocess
from multiprocessing.dummy import Pool
from functools import partial
import os
import argparse


## NOTE: There are a few areas that need to be defined here, marked with ** ** in this code 


# GLOBAL VARIABLES USED THROUGHOUT SCRIPT
bams_file = ""
test = ""
maindir = "" 
scriptsdir = "" 
waspdir = ""
ref_genome_file = ""
ref_genome_bowtie_index = ""
ref_fasta = ""
THREADS = 1


# start() and end() are for printing updates on running program
def start(function):
    print("Starting {}".format(function))

def end(function):
    print("Finished running {}".format(function))


# retrieve all same name from the BAM files
def get_samples(samplefile, num_samples):
    samples = {}

    i = 0
    with open(samplefile, 'r') as f:
        for line in f:
            line = line.rstrip()

            # extract sample name
            name = line.split('execution/')[1]
            name = name.split('.pe')[0]

            samples[name] = line


            if i == num_samples:
                break
            i += 1

    return samples


def runprocess(commands, samples):
    # run the commands in parallel
    pool = Pool(THREADS) # run THREADS concurrent commands
    for i, returncode in enumerate(pool.imap(partial(subprocess.call, shell=True), commands)):
        if returncode != 0:
            print("%d command failed: %d" % (i, returncode))
        print("***FINISHED PROCESSING {} OUT OF {} TOTAL SAMPLES***".format(i, len(commands)))
    


def find_intersecting(samples, snpsdir, intersecting_snps_dir):
    # find the intersecting snsps for each sample BAM with the SNPS
    commands = []

    # build the commands that need to be run    
    for sample in samples:
        bashcommand = "{}/01_intersect_snps.sh {} {} {} {}".format(scriptsdir, snpsdir, intersecting_snps_dir, samples[sample], waspdir)
        commands.append(bashcommand)

    # run the processes in parallel
    runprocess(commands, samples)


def remap_reads(intersecting_snps_dir, remap_dir, samples):
    # remap reads with SNPs replaced
    commands = []

    i = 0
    # build the commands that need to be run
    # do not run the processes in parallel because BOWTIE already does this!!   
    for sample in samples:
        print("***FINISHED PROCESSING {} OUT OF {} TOTAL SAMPLES***".format(i, len(samples)))
        bashcommand = "{}/02_remap_bowtie.sh {} {} {} {}".format(scriptsdir, sample, intersecting_snps_dir, remap_dir, ref_genome_bowtie_index)
        process = subprocess.Popen(bashcommand.split(), stdout = subprocess.PIPE)
        output, error = process.communicate()
        if output:
            print(output)
        if error:
            print(error)
        i += 1

    
def filter_bias(filter_dir, remap_dir, intersecting_snps_dir, samples):
    # filter out the reads that mapped to a different spot
    commands = []

    # build the commands that need to be run    
    for sample in samples:
        bashcommand = "{}/03_filter_reads.sh {} {} {} {} {}".format(scriptsdir, waspdir, sample, filter_dir, intersecting_snps_dir, remap_dir)
        commands.append(bashcommand)

    # run the processes in parallel
    runprocess(commands, samples)

def merge_bams(filter_dir, intersecting_snps_dir, merged_dir, samples):
    # merge the kept reads with those that didn't overlap SNPs
    commands = []

    # build the commands that need to be run    
    for sample in samples:
        bashcommand = "{}/04_merge_bams.sh {} {} {} {}".format(scriptsdir, filter_dir, intersecting_snps_dir, merged_dir, sample)
        commands.append(bashcommand)

    # run the processes in parallel
    runprocess(commands, samples)
        

def remove_dups(rmdup_dir, merged_dir, samples):
    # remove duplicate reads
    commands = []

    # build the commands that need to be run    
    for sample in samples:
        bashcommand = "{}/05_filter_duplicate_reads.sh {} {} {} {}".format(scriptsdir, waspdir, merged_dir, sample, rmdup_dir)
        commands.append(bashcommand)

    # run the processes in parallel
    runprocess(commands, samples)
    
def call_vars(rmdup_dir, mpileup_dir, snpsdir):
    # call variants to get genotype likelihood using mpileup
    # run chromosomes (rather than samples) in parallel
    commands = []

        # chroms = range(1,23)
    chroms = range(1,23)

    # build the commands that need to be run    
    for chrom in chroms:
        # output file
        outfile = "{}/chr{}_mpileup_calls_unfiltered.vcf".format(mpileup_dir, chrom)
        # regions for this chromosome
        regions_file = "{}_vcf/chr{}.snps.vcf.gz".format(snpsdir, chrom)

        bashcommand = "{}/06_variant_calling.sh {} {} {} {}".format(scriptsdir, outfile, rmdup_dir, regions_file, ref_genome_file)
        commands.append(bashcommand)

    # run the processes in parallel
    runprocess(commands, chroms)


def adjust_header(rmdup_dir, adjustheader_dir, samples):
    # adjust the headers in the wasp bam files so that
    # ASEReadCounter can read them in
    commands = []

    # build the commands that need to be run    
    for sample in samples:
        bashcommand = "{}/07_adjust_header.sh {} {} {}".format(scriptsdir, rmdup_dir, sample, adjustheader_dir)
        commands.append(bashcommand)

    # run the processes in parallel
    runprocess(commands, samples)

def asereadcounter(adjustheader_dir, asereadcounter_dir, mpileup_dir, samples):
    # adjust the headers in the wasp bam files so that
    # ASEReadCounter can read them in
    commands = []

    # build the commands that need to be run    
    for sample in samples:
        # for chrom in chroms:
        bashcommand = "{}/08_asereadcounter.sh {} {} {} {} {}".format(scriptsdir, adjustheader_dir, sample, asereadcounter_dir, mpileup_dir, ref_fasta)
        commands.append(bashcommand)

    # run the processes in parallel
    runprocess(commands, samples)


def run_steps(steps, num_samples):
    # settings
    # vcf determines the input format for the SNPs file, 0 = use text format, 1 = vcf format (doesnt work)
    vcf = 0
    global maindir


    # input sample file
    samplefile = bams_file
    # folder containing input SNPs - ** DIRECT THIS TOWARDS INPUT SNPS ** 
    snpsdir = "{}/00_snps_vcf".format(maindir)
    if vcf == 0:
        snpsdir = "{}/00_snps".format(maindir)



    # get samples and their bam paths in a dict (sample: bam path)
    # ** THIS FILE NEEDS TO BE SET UP WITH SAMPLE: BAM PATH ON EACH LINE ** 
    key = "get_samples"
    samples = {}
    start(key)
    samples = get_samples(samplefile, num_samples)
    end(key)


    # find intersecting snps
    key = "find_intersecting"
    intersecting_snps_dir = "{}/01_intersecting_snps".format(maindir)
    if not os.path.exists(intersecting_snps_dir):
        os.makedirs(intersecting_snps_dir)
    if steps[key]:
        start(key)
        find_intersecting(samples, snpsdir, intersecting_snps_dir)
        end(key)

    # realign the new reads
    key = "remap"
    remap_dir = "{}/02_remap".format(maindir)
    if not os.path.exists(remap_dir):
        os.makedirs(remap_dir)
    if steps[key]:
        start(key)
        remap_reads(intersecting_snps_dir, remap_dir, samples)
        end(key)

    # filter out biased reads
    key = "filter_biased_reads"
    filter_dir = "{}/03_filter_remapped_reads".format(maindir)
    if not os.path.exists(filter_dir):
        os.makedirs(filter_dir)
    if steps[key]:
        start(key)
        filter_bias(filter_dir, remap_dir, intersecting_snps_dir, samples)
        end(key)


    # merge the remapped and the keep bams 
    key = "merge_bams"
    merged_dir = "{}/04_merge".format(maindir)
    if not os.path.exists(merged_dir):
        os.makedirs(merged_dir)
    if steps[key]:
        start(key)
        merge_bams(filter_dir, intersecting_snps_dir, merged_dir, samples)
        end(key)

    # filter duplicate reads
    key = "filter_duplicates"
    rmdup_dir = "{}/05_rmdup".format(maindir)
    if not os.path.exists(rmdup_dir):
        os.makedirs(rmdup_dir)
    if steps[key]:
        start(key)
        remove_dups(rmdup_dir, merged_dir, samples)
        end(key)
    
    # call variants to get GL for WASP
    key = "call_vars"
    mpileup_dir = "{}/06_mpileup".format(maindir)
    if not os.path.exists(mpileup_dir):
        os.makedirs(mpileup_dir)
    if steps[key]:
        start(key)
        call_vars(rmdup_dir, mpileup_dir, snpsdir)
        end(key)
    
    # adjust the headers from the WASP filtered reads so ASEReadCounter can read it
    key = "adjust_header"
    adjustheader_dir = "{}/06_adjust_header".format(maindir)
    if not os.path.exists(adjustheader_dir):
        os.makedirs(adjustheader_dir)
    if steps[key]:
        start(key)
        adjust_header(rmdup_dir, adjustheader_dir, samples)
        end(key)

    # adjust the headers from the WASP filtered reads so ASEReadCounter can read it
    key = "asereadcounter"
    asereadcounter_dir = "{}/07_asereadcounter".format(maindir)
    if not os.path.exists(asereadcounter_dir):
        os.makedirs(asereadcounter_dir)
    if steps[key]:
        start(key)
        asereadcounter(adjustheader_dir, asereadcounter_dir, mpileup_dir, samples)
        end(key)

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description='Run the entire mapping pipeline with WASP')
    parser.add_argument('--bams_file', required=True,
            help='file containing paths to input BAM files')
    parser.add_argument('--output_dir', required=True,
            help='main directory to store output')
    parser.add_argument('--scripts_dir', required=True,
            help='directory containing all scripts to run')
    parser.add_argument('--wasp_dir', required=True,
            help='directory containing WASP git')
    parser.add_argument('--ref_genome_bowtie_index', required=True,
            help='Bowtie indexed reference genome file')
    parser.add_argument('--ref_genome_file', required=True,
            help='reference genome file')
    parser.add_argument('--ref_fasta', required=True,
            help='reference genome fasta file')
    parser.add_argument('--threads', required=True,
            help='number of threads to use when running parallel jobs')
    parser.add_argument('--num_samples', required=False, default=-1, type=int,
            help='number of threads to use when running parallel jobs')

    # parse the input arguments
    args = parser.parse_args()
    
    # set up variables with input arguments
    bams_file = args.bams_file
    maindir = args.output_dir
    scriptsdir = args.scripts_dir
    waspdir = args.wasp_dir
    ref_genome_bowtie_index = args.ref_genome_bowtie_index
    ref_genome_file = args.ref_genome_file
    ref_fasta = args.ref_fasta
    THREADS = args.threads


    # define number of samples we're working with
    # used mainly for testing when many samples exist
    # set to -1 to run all samples
    num_samples = args.num_samples

    # ** THIS NEEDS TO BE SET TO RUN SPECFIC PARTS OF THE PIPELINE ** #
    # choose which steps we want to run, 0 = don't run, 1 = run 
    steps = {
        'find_intersecting' : 0,
        'remap' : 0,
        'filter_biased_reads' : 0,
        'merge_bams' : 0,
        'filter_duplicates' : 0, 
        'call_vars' : 0,
        'adjust_header': 0,
        'asereadcounter': 0
    }


    run_steps(steps, num_samples)


if __name__ == '__main__':
    main()

