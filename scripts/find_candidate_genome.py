#!/usr/bin/python3
import os
import sys
from Bio import SeqIO
import textwrap
import matplotlib.pyplot as plt
import numpy as np

output_folder = sys.argv[1]
type_of_genome = sys.argv[2]
fragmented_genome_file = sys.argv[3]

scriptdir =  sys.argv[4]

database = scriptdir+"/../"+"ref_prok_rep_genomes/ref_prok_rep_genomes" if (type_of_genome == "prokaryotic") else "ref_viruses_rep_genomes/ref_viruses_rep_genomes"
print("Using " + database + " database with blastn")

query = output_folder + "/artifacts/ultra_fragmented_genome_file.fna"
output_hits = output_folder + "/artifacts/hits.txt"

query_file = open(query, "a")
fragmented_genome = list(SeqIO.parse(fragmented_genome_file, "fasta"))
for f in fragmented_genome:
    small_fragments = textwrap.wrap(str(f.seq), 10000)
    for i in range(len(small_fragments)):
        query_file.write(">" + f.name + "_" + str(i) + "\n")
        query_file.write(str(small_fragments[i])+ "\n")
query_file.close()

#os.system("ncbi-blast-2.10.0+/blastn -query " + query + " -max_target_seqs 1 -max_hsps 1 -num_threads 8 -outfmt 6 -db " +
os.system(scriptdir+"/../ncbi-blast-2.10.0+/blastn -query " + query + " -max_target_seqs 1 -max_hsps 1 -num_threads 8 -outfmt 6 -db " +
          database + " > " + output_hits)

hits = os.popen("cat " + output_hits).read().split("\n")
probable_genomes = []
probable_genomes_dictionary = dict()
for h in hits:
    if not h:
        continue
    entry = h.split("\t")
    probable_genomes.append([entry[1],entry[3]])
    probable_genomes_dictionary[entry[1]] = 0
for pg in probable_genomes:
    probable_genomes_dictionary[pg[0]] = probable_genomes_dictionary[pg[0]] + int(pg[1])

candidate_genome = list(probable_genomes_dictionary.keys())[0]
for pg in probable_genomes_dictionary:
    if probable_genomes_dictionary[pg] > probable_genomes_dictionary[candidate_genome]:
        candidate_genome = pg

number_of_blasted_fragments = len(list(SeqIO.parse(query, "fasta")))
number_of_aligned_fragments = len(hits) - 1

voting_non_voting_ratio = open(output_folder + "/artifacts/voting_non_voting_fragments.txt", "a")
voting_non_voting_ratio.write("Number of fragments as BLAST input :" + str(number_of_blasted_fragments) + "\n")
voting_non_voting_ratio.write("Number of fragments effectively aligned :" + str(number_of_aligned_fragments) + "\n")
voting_non_voting_ratio.close()


num = len(probable_genomes_dictionary)

names = list(probable_genomes_dictionary.keys())
occurs = list(probable_genomes_dictionary.values())

ind = np.arange(1, num+1)
width = 0.4
fig, ax = plt.subplots()
p1 = ax.bar(ind, list(map(int,occurs)), width, bottom=0)
ax.set_xticks(ind )
ax.set_xticklabels(names)
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
ax.set_title("Found genomes and relative abundance")
ax.set_ylabel('Number of contigs')
ax.set_xlabel('NCBI reference sequence')
plt.tight_layout()
plt.savefig(output_folder + "/artifacts/candidate_genomes.png")

#os.system("ncbi-blast-2.10.0+/blastdbcmd -db " + database + " -entry '" + candidate_genome + "' > " + output_folder + "/artifacts/candidate_genome.fna")
os.system(scriptdir+"/../ncbi-blast-2.10.0+/blastdbcmd -db " + database + " -entry '" + candidate_genome + "' > " + output_folder + "/artifacts/candidate_genome.fna")