#!/bin/bash

basedir= ${PWD}
species=$1
faa=$2

./../diamond makedb --in ${faa} -d ${basedir}/${species}/diamond_refseq

mkdir -p ${basedir}/${species}/Comparison/GFs/diamond_GFs
for x in $(ls ${basedir}/${species}/Comparison/GFs/fasta_GFs) 
do 
echo $x 
./../diamond  blastx -d ${basedir}/${species}/diamond_refseq -q ${basedir}/${species}/Comparison/GFs/fasta_GFs/$x -o ${basedir}/${species}/Comparison/GFs/diamond_GFs/$x.tsv;
done

