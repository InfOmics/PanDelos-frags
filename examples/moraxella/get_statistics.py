#!/usr/bin/python3

import sys

ifile = sys.argv[1]

genomes = set()
genome_codiff = dict()
gene_codiff = dict()


for line in open(ifile, 'r'):
    line = line.strip()
    if len(line) > 0:
        genes = line.split(' ')
        gg = set()
        for gene in genes:
            genome = gene.split(':')[0]
            gg.add(genome)
            genomes.add(genome)
        genome_codiff[len(gg)] = genome_codiff.get(len(gg),0)+1
        gene_codiff[len(genes)] = gene_codiff.get(len(genes),0)+1

for g in sorted(genomes):
    print(g)


print("size of gene families")
print('size','nof families')
for k,v in sorted(gene_codiff.items()):
    print(k,v)

print('-')
print("genes co-diffusion")
print('nof genomes','nof families')
for k,v in sorted(genome_codiff.items()):
    print(k,v)


print(sum(genome_codiff.values()))
