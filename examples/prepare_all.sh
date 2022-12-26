#!/bin/bash

basedir=${PWD}
species='fusobacterium_ulcerans'

# Download metagenome files
./download_files.sh ${basedir}/${species}/sequence_url_opendata.txt ${basedir}/${species}/input/fragmented/

# Download reference file
#./download_files_ref.sh ${basedir}/${species}/reference.txt ${basedir}/${species}/input/complete/ # still have to automate this

# Run Roary
echo 'Running Roary...'
${basedir}/run_roary.sh ${species}

# Run PanDelos
echo 'Running PanDelos...'
${basedir}/run_pandelos.sh ${species}
