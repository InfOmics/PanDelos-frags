#!/bin/bash
rm -rf ref_prok_rep_genomes && mkdir ref_prok_rep_genomes && cd ref_prok_rep_genomes
wget ftp://ftp.ncbi.nlm.nih.gov/blast/db/ref_prok_rep_genomes.??.tar.gz
for f in *.tar.gz
 do
   tar -xvf "$f"
done
rm *.tar.gz

# cd .. && rm -rf ref_viruses_rep_genomes && mkdir ref_viruses_rep_genomes && cd ref_viruses_rep_genomes
# wget ftp://ftp.ncbi.nlm.nih.gov/blast/db/ref_viruses_rep_genomes.tar.gz
# tar -xvf *.tar.gz
# rm *.tar.gz