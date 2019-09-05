#!/bin/bash


python expand_ld.py --snp_pos_bed_file Kunkle.1e-5.bed \
       --outf Kunkle.1e-5.expanded.bed &
python expand_ld.py --snp_pos_bed_file 23andme.1e-5.bed \
       --outf 23andme.1e-5.expanded.bed &

python expand_ld.py --snp_pos_bed_file Kunkle.bed \
       --outf Kunkle.expanded.bed &
python expand_ld.py --snp_pos_bed_file 23andme.bed \
       --outf 23andme.expanded.bed &
