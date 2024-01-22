#!/bin/bash
#source ~/.bashrc
#mamba activate trait-mapper
#export PYTHONPATH=/home/glbrc.org/millican/mambaforge/envs/trait-mapper/lib/python3.1/site-packages:/home/glbrc.org/millican/mambaforge/envs/trait-mapper/lib/python3.11/site-packages
#/home/glbrc.org/millican/repos/microbiome_seq_depth/pydepth/split_runs.py $1 $2

process_16s_files()
{
    fname=$(basename -s "_R1_001.fastq.gz" "$1")
    /home/glbrc.org/millican/repos/microbiome_seq_depth/pydepth/split_runs.py "$fname" "16S"
}

process_ITS_files()
{
    fname=$(basename -s "_R1_001.fastq.gz" "$1")
    /home/glbrc.org/millican/repos/microbiome_seq_depth/pydepth/split_runs.py "$fname" "ITS"
}

export -f process_16s_files
export -f process_ITS_files

find /home/glbrc.org/millican/projects/scri/data/reads/16S/ -name "*_R1_001.fastq.gz" | parallel -j 8 process_16s_files

wait

find /home/glbrc.org/millican/projects/scri/data/reads/ITS/ -name "*_R1_001.fastq.gz" | parallel -j 8 process_ITS_files
