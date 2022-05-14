#!/usr/bin/python3

import os
import pysam
import sys
import numpy as np

genome = sys.argv[1]
output_folder = sys.argv[2]

print('@@@@', output_folder)

input_fasta = output_folder + "/results/" + genome + "_reconstructed_genome.fna"
samfile = pysam.AlignmentFile(output_folder + "/artifacts/sorted_contigs_alignment_on_rgenome.bam", "r")
predicted_file_name = output_folder + "/results/" + genome + "_predictedCDSs"
predicted_filtered_file_name = output_folder + "/results/" + genome + "_predictedCDSs_filtered"
frags_with_no_genes = output_folder + "/results/" + genome + "_frags_with_no_genes.txt"
predicted_filtered_only_genes_file_name = output_folder + "/artifacts/" + genome + "_predictedCDSs_filtered_only_genes.bed"
gene_positions = os.popen("grep 'CDS' " + predicted_file_name + " | awk '{print $2}'").read()

sequence_identifier = os.popen("grep '>' " + input_fasta).read()
sequence_identifier = sequence_identifier[1:-1]
sequence_identifier = sequence_identifier.split(" ")[0]

gene_positions = gene_positions.split("\n")
ref_name = samfile.references[0]
deduced_bases = []
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
    if samfile.count(ref_name, gene[0],gene[1]) > 0 :
        message = "gene positions: " + str(gene) + "\t over contigs positions: "
        uncovered_indices = set(range(gene[0],gene[1]+1))
        for contig in samfile.fetch(ref_name, gene[0],gene[1]):
            message = message + str([contig.reference_start, contig.reference_end]) + "\t"
            uncovered_indices = uncovered_indices.difference(set(range(contig.reference_start,contig.reference_end+1)))
        deduced_bases.append(len(uncovered_indices))
        os.system("echo '" + message + "    -------    # of deduced bases: "  +
                  str(len(uncovered_indices)) + "' >> " + predicted_filtered_file_name)
        start = gene[0]
        start = start - 1
        stop = gene[1]
        strand = "-" if in_reverse_strands else "+"
        os.system("echo '" + sequence_identifier + "\t" + str(start) + "\t" + str(stop) + "\t"
                  + str(len(uncovered_indices)) + "\t" +"1\t" + strand + "' >> " + predicted_filtered_only_genes_file_name)

names = np.unique(np.array(deduced_bases))
unique, counts = np.unique(np.array(deduced_bases), return_counts=True)
os.system("echo '\n\n##############################\n## Summary of deduced bases ##\n##############################\n' >> " + predicted_filtered_file_name)
for element in zip(unique,counts):
    os.system("echo '" + str(element[0]) + " deduced bases in " + str(element[1]) + " genes" + "' >> " + predicted_filtered_file_name)


#How many original fragments do not contain any gene?
gene_ranges = set()
for gene in gene_positions:
    if not gene:
        continue
    if gene.startswith("complement"):
        gene = gene[11:-1]
    temp = gene.split("..")
    temp[0] = temp[0].replace(">", "").replace("<", "")
    temp[1] = temp[1].replace(">", "").replace("<", "")
    gene = [int(temp[0]), int(temp[1])]
    gene_ranges = gene_ranges.union(set(range(int(gene[0]), int(gene[1]) + 1)))
samfile = pysam.AlignmentFile(output_folder + "/artifacts/sorted_contigs_alignment_on_rgenome.bam", "r")
os.system("touch " + frags_with_no_genes)
for fragment in samfile.fetch():
    start = fragment.reference_start
    end = fragment.reference_end
    fragment_range = set(range(start,end))
    if len(fragment_range.intersection(gene_ranges)) < 1:
        os.system("echo '" + fragment.qname + "  length: " + str(len(fragment.seq)) + "' >> " + frags_with_no_genes)