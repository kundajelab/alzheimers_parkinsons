#!/bin/bash
#python generate_resumer_jsons.py --metadata_file_list metadata_list.txt \
#    --resolver_script_path $HOME/atac-seq-pipeline/utils/resumer/resumer.py \
#    --outf resumer_files.txt

python generate_resumer_jsons.py --metadata_file_list metadata_list.txt \
    --resolver_script_path $HOME/chip-seq-pipeline2/utils/resumer/resumer.py \
    --outf resumer_files.txt

