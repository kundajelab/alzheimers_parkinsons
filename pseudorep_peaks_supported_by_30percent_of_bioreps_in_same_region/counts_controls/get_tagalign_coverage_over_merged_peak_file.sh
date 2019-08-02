#!/bin/bash 
bedtools coverage -counts -a $1 -b $2 | cut -f4 >> counts.$3.txt
