#!/usr/bin/env python3
import os
import sys
odir=sys.argv[1]
dirs = os.listdir(odir+'/fragmented/')
if not os.path.exists(odir+'/fragmented_coordinates/'):
    os.mkdir(odir+'/fragmented_coordinates/')

for x in dirs:
    if not os.path.exists(odir+'/fragmented_coordinates/'+x): 
        os.mkdir(odir+'/fragmented_coordinates/'+x)

    out_file = odir+'/fragmented_coordinates/'+x+'/renamed_gene_sequences.fna'
    out = open(out_file, "w")
    with open(odir+'/fragmented/'+x+'/results/gene_sequences.fna') as f:
        lines = f.readlines()
        for l in lines:
            if l.startswith('>'):
                new_name = '>'+l.split('\t')[1].rstrip()
                out.write(new_name+'\n')
            else:
                out.write(l)
