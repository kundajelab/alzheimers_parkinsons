import pdb
from kerasAC.generators.snp_generator import *
from kerasAC.interpret.ism import *
from kerasAC.interpret import load_model 
from kerasAC.interpret import input_grad


alt_gen=SNPGenerator(bed_path="/srv/scratch/annashch/deeplearning/adpd/interpret/SigSNPs_AllClusters_MergedUnique.csv",
                 chrom_col="chr",
                 pos_col="start",
                 allele_col="effect",
                 flank_size=500,
                 rsid_col=None,
                 compute_gc=True,
                 ref_fasta="/mnt/data/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta",
                 batch_size=10)
ref_gen=SNPGenerator(bed_path="/srv/scratch/annashch/deeplearning/adpd/interpret/SigSNPs_AllClusters_MergedUnique.csv",
                 chrom_col="chr",
                 pos_col="start",
                 allele_col="noneffect",
                 flank_size=500,
                 rsid_col=None,
                 compute_gc=True,
                 ref_fasta="/mnt/data/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta",
                 batch_size=10)


                 
