#!/bin/bash
source ~/.bashrc
mamba activate trait-mapper
/home/glbrc.org/millican/repos/microbiome_seq_depth/pydepth/sort_reads.py $1 $2 $3