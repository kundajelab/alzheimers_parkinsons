#!/bin/bash

for i in {2..24}
    do
        echo $i
        cp /users/soumyak/alzheimers_parkinsons/snp_scoring_notebooks/Cluster1.ipynb /users/soumyak/alzheimers_parkinsons/snp_scoring_notebooks/Cluster${i}.ipynb
    done

