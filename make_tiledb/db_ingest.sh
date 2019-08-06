#!/bin/bash
db_ingest --tiledb_metadata tiledb_metadata_adpd.txt \
       --tiledb_group /mnt/lab_data2/projects/adpd/adpd_tiledb \
       --overwrite \
       --chrom_sizes hg38.chrom.sizes \
       --chrom_threads 1 \
       --task_threads 25 \
       --store_summits \
       --summit_indicator 2
