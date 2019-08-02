#!/bin/bash

module load biology
module load bcftools/1.8

bcftools call -c -A -v -O b $1
