#!/bin/bash 
source activate encode-atac-seq-pipeline
caper server --port 8000 --out-dir /oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/pseudobulk/pseudobulk_outputs

