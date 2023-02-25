#!/bin/bash

gdir="PanDelos-fragments/examples/moraxella/input"
odir="PanDelos-fragments/examples/moraxella/output"
ilist="PanDelos-fragments/examples/moraxella/ilist.csv"

if [ -f "$ilist" ]; then
    rm $ilist
fi

mkdir -p $gdir
rm -f -- $gdir/*

mkdir -p $odir
rm -f -- $odir/*

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

#../../pandelos-frags $ilist $odir
