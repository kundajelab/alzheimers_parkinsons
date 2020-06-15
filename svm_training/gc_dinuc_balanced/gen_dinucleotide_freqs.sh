#AGE DATASETS
#balance dinucleotide

python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/nobel_lab_projects/age/deep_learning/age.train.augmented.bed \
	   --outf age.freqs.bed \
	   --ratio_neg_to_pos 10 \
	   --task 0 \
	   --ref /mnt/data/annotations/by_release/mm10/GRCm38.genome.fa

python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/nobel_lab_projects/age/deep_learning/age.train.augmented.bed \
       --outf age.train \
       --ratio_neg_to_pos 10 10 10 10 10 10 10 10 10 10 \
       --dinuc_freqs age.freqs.bed \
       --ref /mnt/data/annotations/by_release/mm10/GRCm38.genome.fa


#DINUCLEOTIDE
#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_se/V576_DNase.train.bed \
#       --outf V57_DNase.train.dinuc.txt \
#       --ratio_neg_to_pos 11 \
#       --ref_fasta hg19.genome.fa
#
#
#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.validate.bed \
#       --outf V57_DNase.validate.gc.txt \
#       --ratio_neg_to_pos 11 \
#       --ref_fasta hg19.genome.fa
#
#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.test.bed \
#       --outf V57_DNase.test.gc.txt \
#       --ratio_neg_to_pos 11 \
#       --ref_fasta hg19.genome.fa
#
#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.test.bed \
#       --outf /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.test.dinuc.balanced.bed \
#       --dinuc_freqs V57_DNase.test.dinuc.txt \
#       --ref_fasta hg19.genome.fa \
#       --ratio_neg_to_pos 11 \
#       --task 0
#
#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.validate.bed \
#       --outf /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.validate.dinuc.balanced.bed \
#       --dinuc_freqs V57_DNase.validate.dinuc.txt \
#       --ref_fasta hg19.genome.fa \
#       --ratio_neg_to_pos 11 \
#       --task 0
#
#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.train.bed \
#       --outf /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.train.dinuc.balanced.bed \
#       --dinuc_freqs V57_DNase.train.dinuc.txt \
#       --ref_fasta hg19.genome.fa \
#       --ratio_neg_to_pos 11 \
#       --task 0
#



#GC CONTENT 
#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.train.bed \
#       --outf V57_DNase.train.gc.txt \
#       --ratio_neg_to_pos 11 \
#       --ref_fasta hg19.genome.fa \
#       --gc


#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.validate.bed \
#       --outf V57_DNase.validate.gc.txt \
#       --ratio_neg_to_pos 11 \
#       --ref_fasta hg19.genome.fa \
#       --gc

#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.test.bed \
#       --outf V57_DNase.test.gc.txt \
#       --ratio_neg_to_pos 11 \
#       --ref_fasta hg19.genome.fa \
#       --gc

#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.test.bed \
#       --outf /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.test.gc.balanced.bed \
#       --dinuc_freqs V57_DNase.test.gc.txt \
#       --ref_fasta hg19.genome.fa \
#       --ratio_neg_to_pos 11 \
#       --task 0 \
#       --gc

#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.validate.bed \
#       --outf /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.validate.gc.balanced.bed \
#       --dinuc_freqs V57_DNase.validate.gc.txt \
#       --ref_fasta hg19.genome.fa \
#       --ratio_neg_to_pos 11 \
#       --task 0 \
#       --gc
#
#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.train.bed \
#       --outf /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_negative_set/V576_DNase.train.gc.balanced.bed \
#       --dinuc_freqs V57_DNase.train.gc.txt \
#       --ref_fasta hg19.genome.fa \
#       --ratio_neg_to_pos 11 \
#       --task 0 \
#       --gc
#
