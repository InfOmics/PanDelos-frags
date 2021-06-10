#!/usr/bin/python3
import os
import sys
from Bio import SeqIO

output_folder = sys.argv[1]
genome = sys.argv[2]

prodigal_output_seqs = list(SeqIO.parse(output_folder + "/prodigal_sequences.fna", "fasta"))
prodigal_filtered_seqs = open(output_folder + "/filtered_prodigal_sequences.fna","a")
for p in prodigal_output_seqs:
    true_boundary = p.description.split("#")[4].split(";")[1].startswith("partial=00")
    if true_boundary:
        description = p.description.split("#")[0]
        g = genome.split("/")[-1].split(".")[0]
        description = ">" + g + "\t" + g + ":" +description + "\tUnknown product"
        prodigal_filtered_seqs.write(description + "\n")
        prodigal_filtered_seqs.write(str(p.seq) + "\n")
prodigal_filtered_seqs.close()