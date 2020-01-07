#!/bin/bash
python group_perf_by_clusters.py --perf_metric_files clusters_gc_classification/perf.* clusters_gc_regression/perf.* --outf cluster.perf.txt
