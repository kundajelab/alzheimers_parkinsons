#!/bin/bash
set -e
GIT_DIR=/home/users/annashch/atac-seq-pipeline
CROMWELL_JAR=/home/users/annashch/cromwell-40.jar
module load java
source activate encode-atac-seq-pipeline
INPUT=$1
PIPELINE_METADATA=metadata.json
NUM_CONCURRENT_TASK=2 # number of replicates
java -jar -Djava.io.tmpdir=/oak/stanford/groups/akundaje/annashch/tmp -Dconfig.file=$GIT_DIR/backends/backend.conf \
-Dbackend.providers.Local.config.concurrent-job-limit=${NUM_CONCURRENT_TASK} \
$CROMWELL_JAR run $GIT_DIR/atac.wdl -i ${INPUT} -m ${PIPELINE_METADATA}
