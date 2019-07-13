#!/bin/bash
python annotate_peak_support.py --peak_set controls/$1.ctr.idr.optimal_set.sorted.merged.bed.gz \
    --supporting_files controls/$1.ctr.optimal.idr.narrowPeak.txt \
    --outf controls_annotated/$1.ctr.optimal.idr.narrowPeak.annotated.txt \
    --base_overlap_thresh 1
