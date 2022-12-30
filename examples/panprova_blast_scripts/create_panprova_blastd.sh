
for fragmentation in 0.5 0.6 0.7 0.8 0.9 1
do 

# create a directory fo blastdb results
mkdir -p /home/claudia/Desktop/ADAIR/PanDelos-frags/myco/DBS_myco_10_leaf_genomes_fragments_${fragmentation}/blastdb

for i in `cat /home/claudia/Desktop/ADAIR/PanDelos-frags/myco/selected_genomes`
do


python3 /home/claudia/Desktop/ADAIR/PanDelos-frags/Blast_claudia/scripts/extract_survival_genes.py /home/claudia/Desktop/ADAIR/PanDelos-frags/myco/DBS_myco_10_leaf_genomes_fragments_${fragmentation}/genome_${i}_fr.log /home/claudia/Desktop/ADAIR/PanDelos-frags/myco/ori/example/ogenomes/genome_${i}.fna /home/claudia/Desktop/ADAIR/PanDelos-frags/myco/ori/example/ogenomes/genome_${i}.gff ${i} /home/claudia/Desktop/ADAIR/PanDelos-frags/myco/DBS_myco_10_leaf_genomes_fragments_${fragmentation}/blastdb/genome_${i}_fr_genes.fna

makeblastdb -in /home/claudia/Desktop/ADAIR/PanDelos-frags/myco/DBS_myco_10_leaf_genomes_fragments_${fragmentation}/blastdb/genome_${i}_fr_genes.fna -out /home/claudia/Desktop/ADAIR/PanDelos-frags/myco/DBS_myco_10_leaf_genomes_fragments_${fragmentation}/blastdb/genome_${i}_fr_genes.fna.blastdb -dbtype nucl
done

done
