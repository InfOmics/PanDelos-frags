#!/bin/bash

gdir="PanDelos-fragments/examples/moraxella/input"
odir="PanDelos-fragments/examples/moraxella/output"
ilist="PanDelos-fragments/examples/moraxella/ilist.csv"

if [ -f "$ilist" ]; then
    rm $ilist
fi

mkdir -p $gdir
rm $gdir/*

mkdir -p $odir
rm $odir/*

for e in `cat PanDelos-fragments/examples/moraxella/moraxella_complete.txt`; do
wget -P "$gdir" $e
e=`basename $e`
gunzip $gdir/$e
e=`echo $e | sed s/\.gz//g`
echo "$gdir/$e    complete" >>$ilist
done

for e in `cat PanDelos-fragments/examples/moraxella/moraxella_fragmented.txt`; do
wget -P "$gdir" $e 
e=`basename $e`
gunzip $gdir/$e
e=`echo $e | sed s/\.gz//g`
echo "$gdir/$e    prokaryotic" >>$ilist
done

#../../pandelos-frags $ilist $odir
