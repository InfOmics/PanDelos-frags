import os
import pysam
import sys
import numpy as np

genome = sys.argv[1]
output_folder = sys.argv[2]

print('@@@@', output_folder)

input_fasta = output_folder + "/results/" + genome + "_reconstructed_genome.fna"
samfile = pysam.AlignmentFile(output_folder + "/artifacts/sorted_contigs_alignment_on_rgenome.bam", "r")
ref_name = samfile.references[0]

bam_info = list()
for read in samfile.fetch(ref_name):
    s = read.reference_start
    e =  read.reference_end
    if s > e:
        t = s
        s = e
        e = t
    bam_info.append((s,e))
bam_info = sorted(bam_info)
bam_max_end = 0
for b in bam_info:
    if b[0] > bam_max_end:
        bam_max_end = b[0]
    if b[1] > bam_max_end:
        bam_max_end = b[1]
bam_covered = [False for i in range(bam_max_end+1)]
for b in bam_info:
    for i in range(b[0],b[1]+1):
        bam_covered[i] = True
print(sum(bam_covered))

def count_covered_positions(start, end):
    if start > end:
        t = end
        end = start
        start = t
    count = 0
    for i in range(start,end+1):
        if len(bam_covered) > i:
            if bam_covered[i]:
                count += 1
    return count

def get_covered_ranges(start, end):
    if start > end:
        t = end
        end = start
        start = t
    ranges = list()
    i = start
    while i < (end+1):
        if bam_covered[i]:
            rstart = i
            j = i+1
            while (j<end+1) and (bam_covered[j]==True):
                j += 1
            if j == len(bam_covered):
                j -= 1
            ranges.append( (rstart,j) )
            i = j+1
        else:
            i += 1
    return ranges

def get_covered_bams(start, end):
    if start > end:
        t = end
        end = start
        start = t
    bams = list()
    for b in bam_info:
        #if start > b[1]:
        #    break
        #else:
            #if (start >= b[0]) and (start<=b[1]):
            #    e = min(end, b[1])
            #    bams.append( (start,e) )
            #elif (end >= b[0]) and (end<=b[1]):
            #    s = max(start,b[0])
            #    bams.append( (s,end) )
            #elif (start<b[0]) and (end>b[1]):
            #    bams.append( (b[0],b[1]) )
        if (start >= b[0]) and (start<=b[1]):
            bams.append( b )
        elif (end >= b[0]) and (end<=b[1]):
            bams.append( b )
        elif (start<b[0]) and (end>b[1]):
            bams.append( b )
    return bams


predicted_file_name = output_folder + "/results/" + genome + "_predictedCDSs"
predicted_filtered_file_name = output_folder + "/results/" + genome + "_predictedCDSs_filtered"
frags_with_no_genes = output_folder + "/results/" + genome + "_frags_with_no_genes.txt"
predicted_filtered_only_genes_file_name = output_folder + "/artifacts/" + genome + "_predictedCDSs_filtered_only_genes.bed"
gene_positions = os.popen("grep 'CDS' " + predicted_file_name + " | awk '{print $2}'").read()

sequence_identifier = os.popen("grep '>' " + input_fasta).read()
sequence_identifier = sequence_identifier[1:-1]
sequence_identifier = sequence_identifier.split(" ")[0]

gene_positions = gene_positions.split("\n")
ref_name = samfile.references[0]
deduced_bases = []

covered_by_genes = [False for i in range(bam_max_end+1)]
deduced_bases = []


predicted_filtered_file_name_off  = open(predicted_filtered_file_name,'w')
predicted_filtered_only_genes_file_name_off = open(predicted_filtered_only_genes_file_name,'w')

for gene in gene_positions:
    #print('-'*40)
    in_reverse_strands = False
    if not gene:
        continue
    if gene.startswith("complement"):
        gene = gene[11:-1]
        in_reverse_strands = True
    temp = gene.split("..")
    temp[0] = temp[0].replace(">", "").replace("<", "")
    temp[1] = temp[1].replace(">", "").replace("<", "")
    gene = [int(temp[0]), int(temp[1])]
    covered_positions = count_covered_positions(gene[0],gene[1])
    uncovered_positions = (gene[1] - gene[0])+1 - covered_positions  

    gstart = gene[0]
    gend = gene[1]
    if gstart > gend:
        t = gend
        gend = gstart
        gstart = t
    for i in range(gstart, gend+1):
        if len(covered_by_genes) > i:
            covered_by_genes[i] = True


    if covered_positions > 0:
        #print(gene)
        covered_bams = get_covered_bams(gstart,gend)
        #print(covered_bams)

        #os.system("echo '" + message + "    -------    # of deduced bases: "  +
        #          str(len(uncovered_indices)) + "' >> " + predicted_filtered_file_name)
        predicted_filtered_file_name_off.write(  "gene positions: ["+str(gstart)+", "+str(gend)+"]   over contigs positions: "+ '\t'.join(  [ "["+str(b[0])+", "+str(b[1])+"]" for b in covered_bams ]  ) +"            -------    # of deduced bases: "+str(uncovered_positions)+"\n"    )

        start = gene[0]
        start = start - 1
        stop = gene[1]
        strand = "-" if in_reverse_strands else "+"
        #os.system("echo '" + sequence_identifier + "\t" + str(start) + "\t" + str(stop) + "\t"
        #          + str(len(uncovered_indices)) + "\t" +"1\t" + strand + "' >> " + predicted_filtered_only_genes_file_name)
        predicted_filtered_only_genes_file_name_off.write( sequence_identifier + "\t" + str(start) + "\t" + str(stop) +"\t"+ str(uncovered_positions) + "\t" +"1\t" + strand+"\n" )

        deduced_bases.append(uncovered_positions)


names = np.unique(np.array(deduced_bases))
unique, counts = np.unique(np.array(deduced_bases), return_counts=True)
#os.system("echo '\n\n##############################\n## Summary of deduced bases ##\n##############################\n' >> " + predicted_filtered_file_name)
predicted_filtered_file_name_off.write('\n\n##############################\n## Summary of deduced bases ##\n##############################\n')
for element in zip(unique,counts):
    #os.system("echo '" + str(element[0]) + " deduced bases in " + str(element[1]) + " genes" + "' >> " + predicted_filtered_file_name)
    predicted_filtered_file_name_off.write(str(element[0]) + " deduced bases in " + str(element[1]) + " genes\n")


predicted_filtered_file_name_off.flush()
predicted_filtered_file_name_off.close()
predicted_filtered_only_genes_file_name_off.flush()
predicted_filtered_only_genes_file_name_off.close()


#How many original fragments do not contain any gene?
#gene_ranges = set()
#for gene in gene_positions:
#    if not gene:
#        continue
#    if gene.startswith("complement"):
#        gene = gene[11:-1]
#    temp = gene.split("..")
#    temp[0] = temp[0].replace(">", "").replace("<", "")
#    temp[1] = temp[1].replace(">", "").replace("<", "")
#    gene = [int(temp[0]), int(temp[1])]
#    gene_ranges = gene_ranges.union(set(range(int(gene[0]), int(gene[1]) + 1)))


samfile.close()
samfile = pysam.AlignmentFile(output_folder + "/artifacts/sorted_contigs_alignment_on_rgenome.bam", "r")
#os.system("touch " + frags_with_no_genes)

frags_with_no_genes_off = open(frags_with_no_genes,'w')

for fragment in samfile.fetch():
    start = fragment.reference_start
    end = fragment.reference_end
    if start > end:
        end = t
        end = start
        start = t

    count = 0
    for i in range(start, end+1):
        if covered_by_genes[i] == True:
            count += 1
            break
    if count == 0:
        frags_with_no_genes_off.write(fragment.qname + "  length: " + str(len(fragment.seq))+"\n")

    #if len(fragment_range.intersection(gene_ranges)) < 1:
        #pass
        #os.system("echo '" + fragment.qname + "  length: " + str(len(fragment.seq)) + "' >> " + frags_with_no_genes)

samfile.close()
frags_with_no_genes_off.close()
