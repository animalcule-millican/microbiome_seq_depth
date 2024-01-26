#!/bin/bash
source ~/.bashrc
#mamba activate trait-mapper
#export PYTHONPATH=/home/glbrc.org/millican/mambaforge/envs/trait-mapper/lib/python3.1/site-packages:/home/glbrc.org/millican/mambaforge/envs/trait-mapper/lib/python3.11/site-packages
#/home/glbrc.org/millican/repos/microbiome_seq_depth/pydepth/split_runs.py $1 $2

process_files()
{
    /home/glbrc.org/millican/repos/microbiome_seq_depth/pydepth/split_runs.py "$1" "$taxa"
    if [ $? -ne 0 ]; then
        echo "Error processing file $1" >&2
        exit 1
    fi
}

export -f process_files
export taxa=$1

find /home/glbrc.org/millican/projects/scri/data/reads/16S -maxdepth 1 -type f -name "*_R1_001.fastq.gz" | parallel -j 32 process_files

if [ $? -ne 0 ]; then
    echo "Error in parallel execution" >&2
    exit 1
fi