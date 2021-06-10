#!/bin/bash
curr_dir=`pwd`
genome=$1
output_folder=$2
fragmented_genome_file=$3

cd $output_folder

cp results/${genome}_reconstructed_genome.fna \
  artifacts/${genome}_reconstructed_genome.fna
cd ./artifacts
bwa index ${genome}_reconstructed_genome.fna
bwa mem -k 100 ${genome}_reconstructed_genome.fna \
  $fragmented_genome_file > contigs_alignment_on_rgenome.sam
samtools view -b -F 2048 contigs_alignment_on_rgenome.sam | \
  samtools view -b -F 256 > contigs_alignment_on_rgenome.bam
samtools sort contigs_alignment_on_rgenome.bam > sorted_contigs_alignment_on_rgenome.bam
samtools index -b sorted_contigs_alignment_on_rgenome.bam

cd ${curr_dir}