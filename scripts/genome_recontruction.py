#!/usr/bin/python3
import os
import sys
import pysam
from Bio import SeqIO

genome = sys.argv[1]
output_folder = sys.argv[2]

reconstructed_genome_name = open(output_folder + "/artifacts/" + genome + "_reconstructed_genome.fna","a")


reference_genome = list(SeqIO.parse(output_folder + "/artifacts/candidate_genome.fna", "fasta"))[0]
samfile = pysam.AlignmentFile(output_folder + "/artifacts/sorted_contigs_alignment.bam", "r")
unmapped = pysam.AlignmentFile(output_folder + "/artifacts/unmapped.sam", "r")
random_code=os.popen("cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 5 | head -n 1").read()
desc = reference_genome.description.split(" ")
reconstructed_genome_name.write(">" + desc.pop(0) + "reconstructed_" + random_code.split("\n")[0] + "\n")
for u in unmapped.fetch():
    reconstructed_genome_name.write(str(u.seq) + "N"*200 + "\n")

current_position = 0
last_contig = 0
unmapped_contigs = 0
for contig in samfile.fetch():
    if current_position >= contig.reference_end:
        continue
    if current_position < contig.reference_start:
        reconstructed_genome_name.write("\n")
        reconstructed_genome_name.write(str(reference_genome.seq[current_position:(contig.reference_start)]) + "\n")
        reconstructed_genome_name.write("\n")
    reconstructed_genome_name.write(contig.seq + "\n")
    current_position = contig.reference_end
    last_contig = contig

reconstructed_genome_name.write("\n")
reconstructed_genome_name.write( str(reference_genome.seq[last_contig.reference_end:]) + "\n")
reconstructed_genome_name.flush()
reconstructed_genome_name.close()

temp_fasta = SeqIO.parse(output_folder + "/artifacts/" + genome + "_reconstructed_genome.fna","fasta")
rewrapped_fasta = open(output_folder + "/results/" + genome + "_reconstructed_genome.fna","w")
SeqIO.write(list(temp_fasta)[0],rewrapped_fasta,"fasta")
samfile.close()
rewrapped_fasta.close()
