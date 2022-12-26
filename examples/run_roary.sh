#!/bin/bash

basedir=${PWD}
species=$1
echo $species

mkdir -p ${basedir}/${species}/Roary

# run prokka on fragmented genomes
for x in $(ls ${basedir}/${species}/input/fragmented) # fasta files
do 
prokka --kingdom Bacteria --outdir ${basedir}/${species}/Roary/prokka/prokka_$x ${basedir}/${species}/input/fragmented/$x
done

# run prokka on complete genomes (if they exist)
if [[ -d ${basedir}/${species}/input/complete ]]
then
    for x in $(ls ${basedir}/${species}/input/complete) # fasta files
    do
    prokka --kingdom Bacteria --outdir ${basedir}/${species}/Roary/prokka/prokka_$x ${basedir}/${species}/input/complete/$x
    done
fi

# put all gff files together
mkdir ${basedir}/${species}/Roary/prokka_gffs

for x in $(ls ${basedir}/${species}/Roary/prokka)
do 
 bs=$(basename $x)
 mv ${basedir}/${species}/Roary/prokka/$x/*gff  ${basedir}/${species}/Roary/prokka_gffs/$bs.gff
done

# run roary
roary -f ${basedir}/${species}/Roary/output -e -n -v ${basedir}/${species}/Roary/prokka_gffs/*.gff



