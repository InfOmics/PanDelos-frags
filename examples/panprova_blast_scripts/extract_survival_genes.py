import sys

def rc(c):
    if c=='A':
        return 'T'
    if c=='T':
        return 'A'
    if c=='G':
        return 'C'
    if c=='C':
        return 'G'
    return c

ilog = sys.argv[1]
ifasta = sys.argv[2]
igff = sys.argv[3]
genomeid = int(sys.argv[4])
ofile = sys.argv[5]


tokeep = set()
for line in open(ilog,'r'):
    if line[0:2] == 'G:':
        cc = line.strip().split(' ')
        if (cc[1] == 'K') or (cc[1]=='P'):
            tokeep.add(int(cc[2]))
print(len(tokeep),'kept genes')



genomeseq = ""
for line in open(ifasta,'r'):
    line = line.strip()
    if line[0] != '>':
        genomeseq += line

off = open(ofile, 'w')

for line in open(igff,'r'):
    line = line.strip()
    if line[0] != '#':
        cc = line.split('\t')
        geneid = int(cc[8].split(';')[0].replace('ID=',''))
        if geneid in tokeep:
            off.write(">("+str(genomeid)+","+str(geneid)+")\n")
            geneseq = genomeseq[ int(cc[3]):int(cc[4]) ].upper()
            if cc[6] == '-':
                geneseq = ''.join(  [ rc(geneseq[i]) for i in range(len(geneseq)-1, -1, -1)       ]   )
            off.write(geneseq+"\n")

off.flush()
off.close()
