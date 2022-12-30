identity=50
tool=PanDelos

basedir=${PWD}
echo $basedir
filedir=${basedir}/../myco
dbbase=${filedir}/../PanProva_myco

for coverage in 0 50 80
do
	
	for fragmentation in 0.5 0.6 0.7 0.8 0.9 
	do

		pf=${filedir}/myco_${fragmentation}/${tool}/output/fragmented #this should be a directory of fastas dirs
		dbdir=${dbbase}/DBS_myco_10_leaf_genomes_fragments_${fragmentation}

		# if it doesn't exist create directory with perc_identity used in blast
		mkdir -p ${dbbase}/mappings
		mkdir -p ${dbbase}/mappings/perc_id_${identity}
		mkdir -p ${dbbase}/mappings/perc_id_${identity}/qcov_${coverage}

		# make sure file does not exist already 
		rm -f ${dbbase}/mappings/perc_id_${identity}/qcov_${coverage}/${tool}_${fragmentation}_output.delos2ori
		rm -f ${dbbase}/mappings/perc_id_${identity}/qcov_${coverage}/${tool}_${fragmentation}_output.ori2delos

		# for each genome
		for d in `ls ${pf}`
		do

			wholegenome=$d  # whole genome file name
			ogenome=`echo $d | sed s/\.fasta//g` # genome name
			d="${pf}/${wholegenome}/results/gene_sequences.fna"

			#prepare for blast (change headers) and create blastdb
			python3 make_blastdbin_pan.py $d ${d}_fixed.fna 
			makeblastdb -in ${d}_fixed.fna -out $pf/$wholegenome/results/gene_sequences.fna.blastdb -dbtype nucl

			# map in both directions
			blastn -query $dbdir/blastdb/${ogenome}_genes.fna -db $pf/$wholegenome/results/gene_sequences.fna.blastdb  -perc_identity ${identity} -qcov_hsp_perc ${coverage} -outfmt 6 > $pf/$wholegenome/ori2delos.out 
			blastn -query $pf/$wholegenome/results/gene_sequences.fna_fixed.fna  -db $dbdir/blastdb/${ogenome}_genes.fna.blastdb -perc_identity ${identity} -qcov_hsp_perc ${coverage} -outfmt 6 > $pf/$wholegenome/delos2ori.out 

			# put all genomes into one file
			cat $pf/$wholegenome/ori2delos.out >> ${dbbase}/mappings/perc_id_${identity}/qcov_${coverage}/${tool}_${fragmentation}_output.ori2delos
			cat $pf/$wholegenome/delos2ori.out >> ${dbbase}/mappings/perc_id_${identity}/qcov_${coverage}/${tool}_${fragmentation}_output.delos2ori
		done

		# create file with bidirectional best hit
		python3 bidirectional_best_blast.py  ${dbbase}/mappings/perc_id_${identity}/qcov_${coverage}/${tool}_${fragmentation}_output.ori2delos ${dbbase}/mappings/perc_id_${identity}/qcov_${coverage}/${tool}_${fragmentation}_output.delos2ori > ${dbbase}/mappings/perc_id_${identity}/qcov_${coverage}/${tool}_${fragmentation}_bbmapping.csv
		#python3 get_stats.py bbmapping.csv  ${dbdir}/survival_families  output.clus

	done
done
