#!/bin/bash

if [ "$#" -ne 1 ]
then
	echo "Illegal number of parameters. Usage ./setup.sh <n_cores>"
	exit 1
fi 

outdir='/PanDelos-frags/ref_prok_rep_genomes'
ftp_path='ftp://ftp.ncbi.nlm.nih.gov/blast/db'
cd $outdir

cores=$1

if [[ ${cores} -ne 1 ]]
then
	echo ${cores}
	echo 'Downloading files...'
	wget --spider ${ftp_path}/ref_prok_rep_genomes.??.tar.gz >> tmp1 2>&1

	cat tmp1 | grep "ref_prok_rep_genomes\...\.tar\.gz..exists" | grep -o 'ref_prok_rep_genomes\...\.tar\.gz' > tmp2
	cat tmp2 | while read line; do echo ${ftp_path}/$line >> tmp3; done
	cat tmp3 | xargs -n 1 -P $cores wget -q
	rm tmp1 tmp2 tmp3
  
else

	wget ${ftp_path}/ref_prok_rep_genomes.??.tar.gz

fi

for f in *.tar.gz
do
  tar -xvf "$f"
  
  if [ $? -ne 0 ]
  then
  	echo 'Download failed, downloading again:'
	rm ${f}
  	wget ${ftp_path}/${f}
	tar -xvf "$f"
  fi

done
rm *.tar.gz

