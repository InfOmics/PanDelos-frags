identity=50
tool=Roary


basedir=${PWD}
filedir=${basedir}/../myco
dbbase=${filedir}/../PanProva_myco

for coverage in 0 50 80
do
	
	for fragmentation in 0.5 0.6 0.7 0.8 0.9 
	do
		pf=${filedir}/myco_${fragmentation}/${tool}/fasta 
		
		#create dir of fastas for panprova blastn
		if ! [[ -d ${basedir}/${species}/input/complete ]]
		then
			mkdir -p ${pf}
			for x in $(ls ${filedir}/myco_${fragmentation}/${tool}/prokka)
			do 
			 bs=$(basename $x)
			 cp ${filedir}/myco_${fragmentation}/${tool}/prokka/$x/*ffn  ${pf}/$bs.fa
			done
		fi
		 
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
			ogenome=`echo $d | sed s/\.fa//g`
			echo $ogenome
			d="${pf}/$d"
			echo $d

			#prepare for blast (change headers) and create blastdb
			mkdir -p $pf/$ogenome/blastdb
			python3 make_blastdbin_roary.py $pf/$ogenome.fa $pf/$ogenome/blastdb/gene_sequences.fna
			makeblastdb -in $pf/$ogenome/blastdb/gene_sequences.fna -out $pf/$ogenome/blastdb/gene_sequences.fna.blastdb -dbtype nucl

			# map in both directions
			blastn -query $dbdir/blastdb/${ogenome}_fr_genes.fna -db $pf/$ogenome/blastdb/gene_sequences.fna.blastdb  -perc_identity ${identity} -qcov_hsp_perc ${coverage} -outfmt 6 > $pf/$ogenome/ori2delos.out
			blastn -query $pf/$ogenome/blastdb/gene_sequences.fna  -db $dbdir/blastdb/${ogenome}_fr_genes.fna.blastdb -perc_identity ${identity} -qcov_hsp_perc ${coverage} -outfmt 6 > $pf/$ogenome/delos2ori.out  

			# put all genomes into one file
			cat $pf/$ogenome/ori2delos.out >> ${dbbase}/mappings/perc_id_${identity}/qcov_${coverage}/${tool}_${fragmentation}_output.ori2delos
			cat $pf/$ogenome/delos2ori.out >> ${dbbase}/mappings/perc_id_${identity}/qcov_${coverage}/${tool}_${fragmentation}_output.delos2ori
		done

		# create file with bidirectional best hit
		python3 bidirectional_best_blast.py ${dbbase}/mappings/perc_id_${identity}/qcov_${coverage}/${tool}_${fragmentation}_output.ori2delos ${dbbase}/mappings/perc_id_${identity}/qcov_${coverage}/${tool}_${fragmentation}_output.delos2ori > ${dbbase}/mappings/perc_id_${identity}/qcov_${coverage}/${tool}_${fragmentation}_bbmapping.csv
		#python3 get_stats.py bbmapping.csv  ${dbdir}/survival_families  output.clus
	done
done
