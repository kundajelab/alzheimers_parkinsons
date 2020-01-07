#!/bin/bash
python get_number_of_samples_that_support_each_regional_peak.py \
    --pseudorep_idr_optimal_peaks pseudorep.idr.optimal.narrowPeaks.txt \
    --biorep_idr_optimal_peaks optimal.idr.narrowPeaks.txt \
    --samples samples.txt \
    --thresh 0.3 
