#!/bin/bash
python annotate_peak_support.py --peak_set all/$1.idr.optimal_set.sorted.merged.bed.gz \
    --supporting_files all/$1.optimal.idr.narrowPeaks.txt \
    --outf all_annotated/$1.optimal.idr.narrowPeak.annotated.txt \
    --base_overlap_thresh 1
