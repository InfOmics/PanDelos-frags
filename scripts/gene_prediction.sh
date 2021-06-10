#!/bin/bash
SCRIPTPATH=`dirname $( realpath $0 )`

genome=$1
output_folder=$2
$SCRIPTPATH/../Prodigal/prodigal -i ${output_folder}/results/${genome}_reconstructed_genome.fna \
  -o ${output_folder}/results/${genome}_predictedCDSs
