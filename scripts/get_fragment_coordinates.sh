#!/bin/bash 
# run after get_fragment_coordinates.py 
odir=$1
genome_dir=${odir}/fragmented
renamed_genome_dir=${odir}/fragmented_coordinates

for x in $(ls $genome_dir)
do
bwa index $genome_dir/$x/original_genome/*_reference_genome.fna
bwa mem $genome_dir/$x/original_genome/*_reference_genome.fna $renamed_genome_dir/$x/renamed_gene_sequences.fna > $renamed_genome_dir/$x/coordinates_frag.sam
done
