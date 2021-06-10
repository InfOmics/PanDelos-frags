#!/usr/bin/python3
import os
import sys

genome = sys.argv[1]
output_folder = sys.argv[2]

input_fasta = output_folder + "/results/" + genome + "_reconstructed_genome.fna"
gene_positions = output_folder + "/artifacts/" + genome + "_predictedCDSs_filtered_only_genes.bed"
output_sequences = output_folder + "/artifacts/gene_sequences.faa"
os.system("bedtools getfasta -fi " + input_fasta + " -fo " + output_sequences + " -bed " + gene_positions + " -s -name")
os.system(" rm " + output_folder + "/results/*.fai")

sequences = os.popen("cat " + output_sequences).read().split("\n")
for s in sequences:
    if not s:
        continue
    if s.startswith(">"):
        seq_name = s[1:]
        genome_name = seq_name.split(":")[2]
        deduced_bases = seq_name.split(":")[0]
        region = seq_name.split(":")[3]
        os.system("echo '>" + genome_name + "\t" + genome_name + ":" + region + "\tUnknown product \t"+ deduced_bases + "' >> " + output_folder + "/results/gene_sequences.fna")
    else:
        os.system("echo '" + s + "' >> " + output_folder + "/results/gene_sequences.fna")