#!/usr/bin/env python3
from Bio import SeqIO
import os
import gzip
import sys
import glob


def split_runs(input_file, split_path):
    run1 = '000000000-KGKJV'
    run2 = '000000000-KGTPY'
    run3 = '000000000-KGK8M'
    run4 = '000000000-KGMFM'
    run5 = '000000000-KGMYV'
    run6 = '000000000-KHNNM'
    runID = ['000000000-KGKJV', '000000000-KGTPY', '000000000-KGK8M', '000000000-KGMFM', '000000000-KGMYV', '000000000-KHNNM']

    with gzip.open(input_file, 'rt') as f:
        filename = os.path.basename(f.name).replace('.fastq.gz', '')
        for record in SeqIO.parse(f, 'fastq'):
            if run1 in record.id or record.description:
                with gzip.open(f'{split_path}/run1/{filename}.run1.fastq.gz', 'wt') as out:
                    SeqIO.write(record, out, 'fastq')
            if run2 in record.id or record.description:
                with gzip.open(f'{split_path}/run2/{filename}.run2.fastq.gz', 'wt') as out:
                    SeqIO.write(record, out, 'fastq')
            if run3 in record.id or record.description:
                with gzip.open(f'{split_path}/run3/{filename}.run3.fastq.gz', 'wt') as out:
                    SeqIO.write(record, out, 'fastq')
            if run4 in record.id or record.description:
                with gzip.open(f'{split_path}/run4/{filename}.run4.fastq.gz', 'wt') as out:
                    SeqIO.write(record, out, 'fastq')
            if run5 in record.id or record.description:
                with gzip.open(f'{split_path}/run5/{filename}.run5.fastq.gz', 'wt') as out:
                    SeqIO.write(record, out, 'fastq')
            if run6 in record.id or record.description:
                with gzip.open(f'{split_path}/run6/{filename}.run6.fastq.gz', 'wt') as out:
                    SeqIO.write(record, out, 'fastq')
def get_input_files(input_file):
    i_name = os.path.basename(input_file)
    dir_path = os.path.dirname(input_file)
    inl = i_name.split('_')
    input_name = '_'.join(inl[:1])
    f_file = glob.glob(f'{dir_path}/{input_name}*R1*')[0]
    r_file = glob.glob(f'{dir_path}/{input_name}*R2*')[0]
    return f_file, r_file, input_name

def main():
    input_file = sys.argv[1]
    taxa = sys.argv[2]
    f_file, r_file, input_name = get_input_files(input_file)

    #f_file = f"/home/glbrc.org/millican/projects/scri/data/reads/{taxa}/{input_name}_R1_001.fastq.gz"
    #r_file = f"/home/glbrc.org/millican/projects/scri/data/reads/{taxa}/{input_name}_R2_001.fastq.gz"
    split_path = f"/home/glbrc.org/millican/repos/microbiome_seq_depth/data/{taxa}/split_runs"
    
    if os.path.exists(f_file) and os.path.exists(r_file):    
        # forward reads
        split_runs(f_file, split_path)
        # reverse reads
        split_runs(r_file, split_path)
    else:
        if not os.path.exists(f_file):
            print(f'Forward reads not found: {f_file}')
        if not os.path.exists(r_file):
            print(f'Reverse reads not found: {r_file}')

if __name__ == '__main__':
    main()