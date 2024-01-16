#!/usr/bin/env python3
import argparse
import concurrent.futures
from Bio import SeqIO
import gzip 
import glob
import os

# functions for the microbiome sequencing depth analysis project
## extract the basename of all the fastq.gz files in the provided directory
## this will create a list of all the file names in the project.
## we will use this for building the split fastq files when we divide reads by sequencing run.
def get_fastq_basenames(dirpath):
    return [os.path.basename(file).replace('.fastq.gz','') for file in glob.glob(os.path.join(dirpath, '*.fastq.gz'))]

## extract the flowcell id information from all sequences of the provided file basename.
## to simplify life, we will rebuild the full file path using the directory provided to the script as the input argument.
def get_run_id(file_name, dirpath):
    filename = os.path.join(dirpath, file_name) + '.fastq.gz'
    id_list = []
    with gzip.open(filename, "rt") as handle:
        for record in SeqIO.parse(handle, "fastq"):
            header = record.id.split(":")[2]
            id_list.append(header)
    return id_list

def sorting_dict(flowcells):
    sort_dict = {}
    sort_dict[flowcells[0]] = 'run1'
    sort_dict[flowcells[1]] = 'run2'
    sort_dict[flowcells[2]] = 'run3'
    sort_dict[flowcells[3]] = 'run4'
    sort_dict[flowcells[4]] = 'run5'
    sort_dict[flowcells[5]] = 'run6'
    return sort_dict

def ensure_dir_exists(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

def create_run_lists():
    run1_list = []
    run2_list = []
    run3_list = []
    run4_list = []
    run5_list = []
    run6_list = []
    return run1_list, run2_list, run3_list, run4_list, run5_list, run6_list

def create_out_files(file_name, dirpath):
    #runs = ['run1', 'run2','run3','run4','run5','run6']
    #run_combo_list = []
    #for i in range(1,6):
    #    combo = list(itertools.combinations(runs, i))
    #    for j in combo:
    #        run_combo_list.append("-".join(j))

    for item in ['run1', 'run2','run3','run4','run5','run6']:
        ensure_dir_exists(f"{dirpath}/{item}")
    out1 = f"{dirpath}/run1/{file_name}_run1.fastq.gz"
    out2 = f"{dirpath}/run2/{file_name}_run2.fastq.gz"
    out3 = f"{dirpath}/run3/{file_name}_run3.fastq.gz"
    out4 = f"{dirpath}/run4/{file_name}_run4.fastq.gz"
    out5 = f"{dirpath}/run5/{file_name}_run5.fastq.gz"
    out6 = f"{dirpath}/run6/{file_name}_run6.fastq.gz"
    return out1, out2, out3, out4, out5, out6


def split_runs(file_name, sorting, dirpath):
    # create empty lists for each run to dump sorted records into
    run1_list, run2_list, run3_list, run4_list, run5_list, run6_list = create_run_lists()
    # create the output files for each run
    out1, out2, out3, out4, out5, out6 = create_out_files(file_name, dirpath)
    # creat the file name.
    filename = os.path.join(dirpath, file_name) + '.fastq.gz'
    # open the file and loop over the records, sorting them into the appropriate list based on the flowcell id found in the header.
    with gzip.open(filename, 'rt') as f:
        for record in SeqIO.parse(f, "fastq"):
            flow = record.description.split(":")[2]
            if sorting[flow] == 'run1':
                run1_list.append(record)
            elif sorting[flow] == 'run2':
                run2_list.append(record)
            elif sorting[flow] == 'run3':
                run3_list.append(record)
            elif sorting[flow] == 'run4':
                run4_list.append(record)
            elif sorting[flow] == 'run5':
                run5_list.append(record)
            elif sorting[flow] == 'run6':
                run6_list.append(record)
    with gzip.open(out1, 'at') as out_1, gzip.open(out2, 'at') as out_2, gzip.open(out3, 'at') as out_3, gzip.open(out4, 'at') as out_4, gzip.open(out5, 'at') as out_5, gzip.open(out6, 'at') as out_6:
        SeqIO.write(run1_list, out_1, "fastq")
        SeqIO.write(run2_list, out_2, "fastq")
        SeqIO.write(run3_list, out_3, "fastq")
        SeqIO.write(run4_list, out_4, "fastq")
        SeqIO.write(run5_list, out_5, "fastq")
        SeqIO.write(run6_list, out_6, "fastq")


def parse_args():
    parser = argparse.ArgumentParser(description='Sort fastq files by flowcell and lane')
    parser.add_argument('-i', '--input', help='Input fastq file', required=True)
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    fastq_names = get_fastq_basenames(args.input)
    flowcell_list = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_run_id = {executor.submit(get_run_id, file_name, args.input): file_name for file_name in fastq_names}
        for future in concurrent.futures.as_completed(future_to_run_id):
            file_name = future_to_run_id[future]
            try:
                flowcell_list.extend(future.result())
            except Exception as exc:
                print(f'{file_name} generated an exception: {exc}')
    flowcells = list(set(flowcell_list))
    sort_dict = sorting_dict(flowcells)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_split_runs = {executor.submit(split_runs, file_name, sort_dict, args.input): file_name for file_name in fastq_names}
        for future in concurrent.futures.as_completed(future_to_split_runs):
            file_name = future_to_split_runs[future]
            try:
                future.result()
            except Exception as exc:
                print(f'{file_name} generated an exception: {exc}')

if __name__ == '__main__':
    main()