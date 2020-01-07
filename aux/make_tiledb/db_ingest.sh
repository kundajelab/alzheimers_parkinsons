#!/bin/bash
#bulk 
#db_ingest --tiledb_metadata tiledb_metadata_adpd_bulk.txt \
#       --tiledb_group /mnt/lab_data2/projects/adpd/adpd_tiledb_bulk \
#       --overwrite \
#       --chrom_sizes hg38.chrom.sizes \
#       --chrom_threads 1 \
#       --task_threads 25

#pseudobulk
#db_ingest --tiledb_metadata tiledb_metadata_adpd_pseudobulk.txt \
#       --tiledb_group /mnt/lab_data2/projects/adpd/adpd_tiledb_pseudobulk \
#       --chrom_sizes hg38.chrom.sizes \
#       --chrom_threads 2 \
#       --task_threads 5 \
#       --overwrite

#pseudobulk cluster 24 (microglia)
db_ingest --tiledb_metadata tiledb_metadata_adpd_cluster24.txt \
       --tiledb_group adpd_tiledb_pseudobulk \
       --chrom_sizes hg38.chrom.sizes \
       --chrom_threads 20 \
       --task_threads 1 \
       --write_threads 2 \
       --chunk_size 100 \
       --overwrite
