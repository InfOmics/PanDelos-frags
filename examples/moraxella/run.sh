#!/usr/bin/bash

gdir="input_genomes"
odir="result"
ilist="ilist.csv"

if [ -f "$ilist" ]; then
    rm $ilist
fi

mkdir -p $gdir
rm $gdir/*

mkdir -p $odir
rm $odir/*

for e in `cat moraxella_complete.txt`; do
wget -P "$gdir" $e 
e=`basename $e`
gunzip $gdir/$e
e=`echo $e | sed s/\.gz//g`
echo "$gdir/$e    complete" >>$ilist
done

for e in `cat moraxella_fragmented.txt`; do
wget -P "$gdir" $e 
e=`basename $e`
gunzip $gdir/$e
e=`echo $e | sed s/\.gz//g`
echo "$gdir/$e    prokaryotic" >>$ilist
done


../../padelos-frags $ilist $odir