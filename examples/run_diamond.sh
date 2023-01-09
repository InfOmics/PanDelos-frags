#!/bin/bash

basedir=${PWD}
species=$1
faa=$2

echo ${basedir}
echo $species
echo ${faa}
./../diamond makedb --in ${faa} -d ${basedir}/${species}/diamond_refseq

mkdir -p ${basedir}/${species}/Comparison/GFs/diamond
for x in $(ls ${basedir}/${species}/Comparison/GFs/fasta) 
do 
echo $x 
./../diamond  blastx -d ${basedir}/${species}/diamond_refseq -q ${basedir}/${species}/Comparison/GFs/fasta/$x -o ${basedir}/${species}/Comparison/GFs/diamond/$x.tsv;
done

