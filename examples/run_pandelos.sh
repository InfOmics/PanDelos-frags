#!/bin/bash

#conda activate python_env
basedir=${PWD}
ilist="ilist.csv"  
species=$1
tool=${basedir}/../pandelos-frags

mkdir -p ${basedir}/${species}/PanDelos/
mkdir -p ${basedir}/${species}/PanDelos/output
rm -r ${basedir}/${species}/PanDelos/output/*

if [ -f ${basedir}/${species}/PanDelos/${ilist} ]; then
    rm ${basedir}/${species}/PanDelos/${ilist}
fi
 

for e in $(ls ${basedir}/${species}/input/fragmented); do
#e=`basename $e`
echo "${basedir}/${species}/input/fragmented/${e}    prokaryotic" >> ${basedir}/${species}/PanDelos/${ilist}
done



for e in $(ls ${basedir}/${species}/input/complete); do
#e=`basename $e`
echo "${basedir}/${species}/input/complete/${e}    complete" >> ${basedir}/${species}/PanDelos/${ilist}
done
 

bash ${tool} ${basedir}/${species}/PanDelos/${ilist} ${basedir}/${species}/PanDelos/output
