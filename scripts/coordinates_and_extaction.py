#!/usr/bin/python3

import os
import sys
output_folder = sys.argv[1]
genome = sys.argv[2]

sequence_identifier = os.popen("grep '>' " + genome).read()
sequence_identifier = sequence_identifier[1:-1]
sequence_identifier = sequence_identifier.split(" ")[0]

gene_positions = os.popen("grep 'CDS' " + output_folder + "/ProdigalOutput.txt | awk '{print $2}'").read().split("\n")
for gene in gene_positions:
    in_reverse_strands = False
    if not gene:
        continue
    if gene.startswith("complement"):
        gene = gene[11:-1]
        in_reverse_strands = True
    temp = gene.split("..")
    temp[0] = temp[0].replace(">", "").replace("<", "")
    temp[1] = temp[1].replace(">", "").replace("<", "")
    gene = [int(temp[0]), int(temp[1])]
    start = gene[0]
    start = start - 1
    stop = gene[1]
    strand = "-" if in_reverse_strands else "+"
    os.system("echo '" + sequence_identifier + "\t" + str(start) + "\t" + str(stop) + "\t"
              + "seq_name" + "\t" + "1\t" + strand + "' >> " + output_folder + "/coordinates.bed")

os.system("bedtools getfasta -fi " + genome + " -fo " + output_folder + "/gene_sequences_temp.fna" +
          " -bed " + output_folder + "/coordinates.bed" + " -s -name")

sequences = os.popen("cat " + output_folder + "/gene_sequences_temp.fna").read().split("\n")
for s in sequences:
    if not s:
        continue
    if s.startswith(">"):
        seq_name = s[1:]
        genome_name = seq_name.split(":")[2]
        region = seq_name.split(":")[3]
        os.system("echo '>" + genome_name + "\t" + genome_name + ":" + region + "\tUnknown product \t" +
                  "' >> " + output_folder + "/gene_sequences.fna")
    else:
        os.system("echo '" + s + "' >> " + output_folder + "/gene_sequences.fna")

os.system("rm " + output_folder + "/gene_sequences_temp.fna")
os.system("rm " + output_folder + "/coordinates.bed")