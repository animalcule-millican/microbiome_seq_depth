#!/usr/bin/env python3
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import gzip 
import sys
import glob
import os
import pickle
import itertools
import concurrent.futures

def get_file_list(input_dir):
    """
    Get a list of all the fastq.gz files in the provided input directory.
    This should be a list of all the samples sequenced with all the runs concatenated together.
    """
    file_list = glob.glob(f"{input_dir}/*.fastq.gz")
    return file_list

def get_file_run_info(input_file):
    """
    Extract all the important information from the fastq.gz file.
    This includes the basename of the input file, the unique run identifier (which is part of the header), header (or record.id from biopython), sequence, quality scores, and description (the full header of the sequence).
    """
    info_dict = {}
    bname = os.path.basename(input_file).replace(".fastq.gz", "")
    with gzip.open(input_file, "rt") as handle:
        for record in SeqIO.parse(handle, "fastq"):
            info_dict[f"{bname}_{record.description}"] = {"file": input_file, "basename": bname, "runID": record.id.split(":")[2], "header": record.id, "seq": record.seq, "qual": record.letter_annotations["phred_quality"], "description": record.description}
    return info_dict


def sort_runs(input_dict):
    """
    Sort the reads into separate dictionaries based on the runID.
    These  runIDs are unique to this set of samples. The set will have to be updated if applied to a different set of sequence files.
    """
    run_list = set(['000000000-KGKJV', '000000000-KGTPY', '000000000-KGK8M', '000000000-KGMFM', '000000000-KGMYV', '000000000-KHNNM'])
    run_1 = {}
    run_2 = {}
    run_3 = {}
    run_4 = {}
    run_5 = {}
    run_6 = {}
    for key in input_dict:
        if input_dict[key]["runID"] == "000000000-KGKJV":
            run_1[key] = input_dict[key]
        elif input_dict[key]["runID"] == "000000000-KGTPY":
            run_2[key] = input_dict[key]
        elif input_dict[key]["runID"] == "000000000-KGK8M":
            run_3[key] = input_dict[key]
        elif input_dict[key]["runID"] == "000000000-KGMFM":
            run_4[key] = input_dict[key]
        elif input_dict[key]["runID"] == "000000000-KGMYV":
            run_5[key] = input_dict[key]
        elif input_dict[key]["runID"] == "000000000-KHNNM":
            run_6[key] = input_dict[key]
    return run_1, run_2, run_3, run_4, run_5, run_6
    
def write_reads_by_run(input_dict, output_dir, run):
    with open(f"{output_dir}/{run}/{input_dict[key]["basename"]}-{run}.fastq", "w") as handle:
        for key in input_dict:
            seq_record = SeqRecord(Seq(input_dict[key]["seq"]), id=input_dict[key]["header"], description=input_dict[key]["description"], letter_annotations={"phred_quality": input_dict[key]["qual"]})
            SeqIO.write(seq_record, handle, "fastq")

def generate_combinations(file_directory):
    items = glob.glob(f"{file_directory}/run*")
    #items = ['000000000-KGKJV', '000000000-KGTPY', '000000000-KGK8M', '000000000-KGMFM', '000000000-KGMYV', '000000000-KHNNM']
    count = 0
    combo_dict = {}
    for n in range(1, len(items) + 1):
        for i, combination in enumerate(itertools.combinations(items, n)):
            count += 1
            combo_dict[f"combo_{count}"] = combination
    return combo_dict

def write_run_combos(combo_dict, dirpath, key):
    cname = f"run_{key}"
    run_file = f"{dirpath}/{key}.fastq.gz"
    for item in combo_dict[key]:
        file_list = glob.glob(f"{item}/*.fastq.gz")
        file_num = len(glob.glob(f"{item}/*.fastq.gz"))
        with gzip.open(run_file, 'a') as f:
            for i in range(0, len(file_list)):
                with gzip.open(file_list[i], 'rb') as infile:
                    for record in SeqIO.parse(infile, "fastq"):
                        SeqIO.write(record, f, "fastq")

def checkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    read_dict = {}
    in_dir = sys.argv[1]
    output_pickle = sys.argv[2]
    out_dir = sys.argv[3]

    dirpath = f"{out_dir}/run_combinations"
    checkdir(dirpath)
    checkdir(out_dir)
    

    filelist = get_file_list(in_dir)

    with concurrent.futures.ProcessPoolExecutor(max_workers=24) as executor:
        for result in executor.map(get_file_run_info, filelist):
            read_dict.update(result)

    with open(output_pickle, "wb") as handle:
        pickle.dump(read_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    run_1, run_2, run_3, run_4, run_5, run_6 = sort_runs(read_dict)

    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
        executor.map(write_reads_by_run, [run_1, run_2, run_3, run_4, run_5, run_6], [out_dir] * 6, ["run_1", "run_2", "run_3", "run_4", "run_5", "run_6"])

    combo_dict = generate_combinations(out_dir)
    # {output_dir}/{run}

    with concurrent.futures.ProcessPoolExecutor(max_workers=24) as executor:
        executor.map(write_run_combos, combo_dict, dirpath, combo_dict.keys())

if __name__ == "__main__":
    main()