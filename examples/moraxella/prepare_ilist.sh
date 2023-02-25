#!/bin/bash

input_path=$1
gdir=$input_path/data
ilist=$input_path/ilist.csv

if [ -f "$ilist" ]; then
    rm $ilist
fi

mkdir -p $gdir
rm -rf -- $gdir/*

for e in `cat PanDelos-frags/examples/moraxella/moraxella_complete.txt`; do
wget -P "$gdir" $e
e=`basename $e`
gunzip $gdir/$e
e=`echo $e | sed s/\.gz//g`
echo "$gdir/$e,complete" >>$ilist
done

for e in `cat PanDelos-frags/examples/moraxella/moraxella_fragmented.txt`; do
wget -P "$gdir" $e 
e=`basename $e`
gunzip $gdir/$e
e=`echo $e | sed s/\.gz//g`
echo "$gdir/$e,fragmented" >>$ilist
done

