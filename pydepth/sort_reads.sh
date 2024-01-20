#!/bin/bash
source ~/.bashrc
mamba activate trait-mapper
export PYTHONPATH=/home/glbrc.org/millican/mambaforge/envs/trait-mapper/lib/python3.1/site-packages:/home/glbrc.org/millican/mambaforge/envs/trait-mapper/lib/python3.11/site-packages
/home/glbrc.org/millican/repos/microbiome_seq_depth/pydepth/sort_reads.py $1 $2 $3