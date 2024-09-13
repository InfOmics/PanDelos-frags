# PanDelos-frags: a methodology for discovering pangenomic content of incomplete microbial assemblies

## Abstract
Pangenomics was originally defined as the problem of comparing the compo-
sition of genes into gene families within a set of bacterial isolates belonging
to the same species. The problem requires the calculation of sequence ho-
mology among such genes. When combined with metagenomics, namely
for human microbiome composition analysis, gene-oriented pangenome de-
tection becomes a promising method to decipher ecosystem functions and
population-level evolution.
Established computational tools are able to investigate the genetic con-
tent of isolates for which a complete genomic sequence is available. However,
there is a plethora of incomplete genomes that are available on public re-
sources, which only a few tools may analyse. Incomplete means that the
process for reconstructing their genomic sequence is not complete, and only
fragments of their sequence are currently available. However, the information
contained in these fragments may play an essential role in the analyses.
Here, we present PanDelos-frags, a computational tool which exploits and
extends previous results in analysing complete genomes. It provides a new
methodology for inferring missing genetic information and thus for managing
incomplete genomes. PanDelos-frags outperforms state-of-the-art approaches
in reconstructing gene families in synthetic benchmarks and in a real use case
of metagenomics

![Workflow](https://github.com/Cengoni/PanDelos-frags-SUPP/blob/main/workflow.png)

## Using PanDelos-frags
In order to run PanDelos-frags you can download the docker image with all required dependencies installed. 
Once the docker is up and running there are two main steps to get ready to run the tool are:
* download the database of reference sequences (only the first time you use the tool)
* prepare input data 

In the following lines you will see an example of how to get the tool to work and what is the expected input data.

### Download docker image
`docker pull cmengoni/pandelos-frags`

### 1) Run docker

`docker run -it --rm -v <absolute_path_db>:/PanDelos-frags/ref_prok_rep_genomes -v <absolute_path_workingdir>:/<container_workingdir> cmengoni/pandelos-frags`

This command allows you to create a running PanDelos-frags Docker container. In detail:
* `-it`: create an interactive docker container
* `--rm`: the running instance of the container will be removed after it is closed
* `-v <absolute_path_db>:/PanDelos-frags/ref_prok_rep_genomes`: it creates a connection between the local directory where you want to store the database required to run PanDelos-frags (left side, before the double dots) and its corresponding location in the container (right side, after the double dots). It is mandatory that you use the as database path of the container `/PanDelos-frags/ref_prok_rep_genomes`.
* `-v <absolute_path_workingdir>:/<container_workingdir>`: it creates a connection between the local directory where you want to store all files (input/output) related to a specific PanDelos-frags run (left side, before the double dots) and its corresponding location in the container (right side, after the double dots).
In this example

### 2) Run setup.sh script to download database
`./PanDelos-frags/setup.sh <n_cores>`

This script downloads a database of all prokaryotes reference genomes (~18GB)
Note that the database will persist locally even after you stop the container. This will allow you to skip this step in future PanDelos-frags runs.
If you have multiple cores available you can run this script in parallel by adding as `<n_cores>` a number greater than 1 (suggested 18 cores), otherwise just write 1.

### 3) Download input data to run an example
`./PanDelos-frags/examples/moraxella/prepare_ilist.sh <container_workingdir>`

This script downloads 20 Moraxella genomes from NCBI into the input directory `<container_workingdir>/data`. It also creates the input file `<container_workingdir>/ilist.csv` required to run PanDelos-frags. 
In short the `ilist.csv` file is a comma-separated file where the first column contains all the paths to the genomes and the second column contains one of `complete` or `fragmented`, depending on whether the genome is a single-sequence fasta file (`complete`) or a multi-fasta file (`fragmented`).

Example:
```
PanDelos-frags/examples/moraxella/input/GCF_003971285.1_ASM397128v1_genomic.fna,complete
PanDelos-frags/examples/moraxella/input/GCF_003971345.1_ASM397134v1_genomic.fna,complete
PanDelos-frags/examples/moraxella/input/GCF_010603965.1_ASM1060396v1_genomic.fna,fragmented
PanDelos-frags/examples/moraxella/input/GCF_010612395.1_ASM1061239v1_genomic.fna,fragmented
```

### 4) Run PanDelos-frags
`pandelos-frags <container_workingdir>/ilist.csv <container_workingdir>/<ouput_dir>`

This is the actual PanDelos-frags command you need to use to run the tool. The required parameters are an:
* `ilist.csv` input file, formatted as described in the previous point
* an output directory. It's important that the output directory is in the `<container_workingdir>` so that the output will be saved in a container folder which is linked to your local directory. In this way the ouput will persist even after you close the docker container.


## Notes
Once the database has been built you can run PanDelos-frags on your own data structured as an ilist.csv file just by running the docker (step 1) and then running the tool (step 4). Just make sure that the `ilist.csv` file is in a directory that you have linked in the container, so that the output persists.

## Output structure
The main output file is `output.clus`, created in the main output directory. This file is a space-separated file where each line represents a gene family. The genes are represented by a code used throughout the analysis (e.g. NC_000908.2reconstructed_45tua:101242-101644(+)) which contains the genome of belonging (e.g. NC_000908.2reconstructed_45tua) and its location on the genome (e.g. 101242-101644(+)). 
The directories `complete/` and `fragmented/` contain all the relative intermediate file generated by PanDelos-frags.

## Supplementary files
Supplementary scripts and data used to run the analysis reported in PanDelos-frags manuscript can be found at [Cengoni/PanDelos-frags-SUPP](https://github.com/Cengoni/PanDelos-frags-SUPP)

## References
If you have used any of the PanDelos-frags project software, please cite the following paper:

     Vincenzo Bonnici, Claudia Mengoni, Manuel Mangoni, Giuditta Franco, Rosalba Giugno
     PanDelos-frags: A methodology for discovering pangenomic content of incomplete microbial assemblies
     Journal of Biomedical Informatics, Volume 148, December 2023. https://doi.org/10.1016/j.jbi.2023.104552
