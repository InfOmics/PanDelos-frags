#!/bin/bash
curr_dir=`pwd`
output_folder=$2
odir=$2
fragmented_genome_file=$3

#cd $output_folder
pwd

bwa index $odir/artifacts/candidate_genome.fna
echo "-"
bwa mem $odir/artifacts/candidate_genome.fna $fragmented_genome_file > $odir/artifacts/contigs_alignment.sam
echo "-"
samtools view -b -F 256 $odir/artifacts/contigs_alignment.sam | samtools view -b -F 2048  \
  > $odir/artifacts/contigs_alignment.bam
echo "-"
samtools view -h -f 4 $odir/artifacts/contigs_alignment.sam > $odir/artifacts/unmapped.sam
echo "-"
samtools sort $odir/artifacts/contigs_alignment.bam > $odir/artifacts/sorted_contigs_alignment.bam
echo "-"
samtools index -b $odir/artifacts/sorted_contigs_alignment.bam
echo "-"

#cd ${curr_dir}
