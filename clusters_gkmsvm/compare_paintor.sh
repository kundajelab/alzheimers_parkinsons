#!/bin/bash

for i in {1..129}
    do
    if [[ -f /mnt/lab_data3/soumyak/adpd/paintor/no_annot/locus${i}.processed.onlysnps ]]
        then
        result=$(diff /mnt/lab_data3/soumyak/adpd/paintor/no_annot/locus${i}.processed.onlysnps /mnt/lab_data3/soumyak/adpd/paintor/only_atac/locus${i}.processed.onlysnps)
        if [[ $result != '' ]]
            then
            echo Locus $i
        fi
    fi
done
