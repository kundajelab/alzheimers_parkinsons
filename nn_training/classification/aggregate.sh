CLUSTER=$1
python ~/kerasAC/scripts/aggregate_summaries.py --file_name_prefix Cluster$CLUSTER/performance.DNASE.$CLUSTER.classificationlabels.withgc. --file_name_suffix '' --outf perf.$CLUSTER.classification.gc.tsv
