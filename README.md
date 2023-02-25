# PanDelos-frags
A version of PanDelos that discovers pangenomic content in fragmented genomes.

## Using PanDelos-frags
In order to run PanDelos-frags you can download the docker image with all required dependencies installed. 
Once the docker is up and running there are two main steps to get ready to run the tool are:
* download the database of reference sequences (only the first time you use the tool)
* prepare input data 

In the following lines you will see an example of how to get the tool to work and what is the expected input data.
 
## CASE A: First time running PanDelos-frags

### 0) Download docker image
`docker pull cmengoni/pandelos-frags`

### 1) Run docker

`docker run -it --rm -v <absolute_path_db>:/PanDelos-frags/ref_prok_rep_genomes -v <absolute_path_workingdir>:/<container_workingdir> cmengoni/pandelos-frags`

This command allows you to create a running PanDelos-frags Docker container. In detail:
* `-it`: create an interactive docker container
* `--rm`: the running instance of the container will be removed after it is closed
* `-v <absolute_path_db>:/PanDelos-frags/ref_prok_rep_genomes`: it creates a connection between the local directory where you want to store the database required to run PanDelos-frags (left side, before the double dots) and its corresponding location in the container (right side, after the double dots). It is mandatory that you use the as database path of the container `/PanDelos-frags/ref_prok_rep_genomes`.
* `-v <absolute_path_workingdir>:/<container_workingdir>`: it creates a connection between the local directory where you want to store all files related to a specific PanDelos-frags run (left side, before the double dots) and its corresponding location in the container (right side, after the double dots).
In this example

### 2) Run setup.sh script to download database
`./PanDelos-frags/setup.sh <n_cores>`

This script downloads a database of all prokaryotes reference genomes (~18GB)
Note that the database will persist locally even after you stop the container. This will allow you to skip this step in future PanDelos-frags runs.
If you have multiple cores available you can run this script in parallel by adding as `<n_cores>` a number greater than 1 (suggested 18 cores), otherwise just write 1.

### 3) Download input data to run an example
`./PanDelos-frags/examples/moraxella/prepare_ilist.sh`

This script allows you to download 10 Moraxella genomes from a NCBI (cite?) and creates the input file `ilist.csv` required by PanDelos-frags.
You can see the results of running this script in `./PanDelos-fragments/examples/moraxella/ilist.txt`. 
In short the ilist file is a comma-separated file where the first column contains all the paths to the genomes and the second column contains one of `complete` or `fragmented`, depending on whether the genome is a single-sequence fasta file (`complete`) or a multi-fasta file (`fragmented`).

Example:






