#!/bin/bash
#db_ingest --tiledb_metadata tiledb_metadata_adpd_pseudobulk.txt \
#       --tiledb_group /mnt/lab_data2/projects/adpd/adpd_tiledb_pseudobulk \
#       --chrom_sizes hg38.chrom.sizes \
#       --chrom_threads 1 \
#       --task_threads 1 \
#       --overwrite \
#       --write_threads 50 
##exclude microglia (cluster 24) because it has been processed already
db_ingest --tiledb_metadata tiledb_metadata_adpd_pseudobulk_NO_cluster24.txt \
       --tiledb_group /mnt/lab_data2/projects/adpd/adpd_tiledb_pseudobulk \
       --chrom_sizes hg38.chrom.sizes \
       --chrom_threads 1 \
       --task_threads 1 \
       --overwrite \
       --write_threads 50 

