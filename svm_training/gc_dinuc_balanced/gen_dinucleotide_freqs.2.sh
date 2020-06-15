#EASY DATASET QC
#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/easy.V576.source.bed \
#       --outf /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/V576.dinuc.1neg.1pos.txt \
#       --ratio_neg_to_pos 1 \
#       --ref_fasta hg19.genome.fa

#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/easy.V576.source.bed \
#       --outf /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/V576.dinuc.5neg.1pos.txt \
#       --ratio_neg_to_pos 5 \
#       --ref_fasta hg19.genome.fa &
#
#
#
#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/easy.V576.source.bed \
#       --outf /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/V576.gc.1neg.1pos.txt \
#       --ratio_neg_to_pos 1 \
#       --ref_fasta hg19.genome.fa \
#       --gc &
#
#
#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/easy.V576.source.bed \
#       --outf /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/V576.gc.5neg.1pos.txt \
#       --ratio_neg_to_pos 5 \
#       --ref_fasta hg19.genome.fa \
#       --gc &
#

#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/easy.V576.source.bed \
#       --outf /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/V576.dinuc.1neg.1pos.bed \ 
#       --ratio_neg_to_pos 1 \
#       --dinuc_freqs /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/V576.dinuc.1neg.1pos.txt \
#       --ref_fasta hg19.genome.fa &
#
python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/easy.V576.source.bed \
       --outf /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/V576.dinuc.5neg.1pos.bed \
       --ratio_neg_to_pos 5 \
       --dinuc_freqs /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/V576.dinuc.5neg.1pos.txt \
       --ref_fasta hg19.genome.fa 


#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/easy.V576.source.bed \
#       --outf /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/V576.gc.1neg.1pos.bed \
#       --dinuc_freqs /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/V576.gc.1neg.1pos.txt \
#       --ratio_neg_to_pos 1 \
#       --task 0 \
#       --ref_fasta hg19.genome.fa \
#       --gc
#
#
#python gen_dinucleotide_freqs.py --bed_path /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/easy.V576.source.bed \
#       --outf /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/V576.gc.5neg.1pos.bed \
#       --dinuc_freqs /srv/scratch/annashch/deeplearning/form_inputs/gecco_inputs_v2/experiments_easy_set/V576.gc.5neg.1pos.txt \
#       --ratio_neg_to_pos 5 \
#       --ref_fasta hg19.genome.fa \
#       --task 0 \
#       --gc
#

