import sys

ifile = sys.argv[1]
ofile = sys.argv[2]

off = open(ofile, 'w')


for line in open(ifile,'r'):
    if line[0] == '>':
        cc = line.split('\t')[1]
        off.write(">"+cc+"\n")
    else:
        off.write(line)


off.flush()
off.close()
