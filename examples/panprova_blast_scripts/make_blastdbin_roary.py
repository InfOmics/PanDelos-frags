import sys

ifile = sys.argv[1]
ofile = sys.argv[2]

off = open(ofile, 'w')


for line in open(ifile,'r'):
    if line[0] == '>':
        cc = line.split(' ')[0]
        off.write(cc+"\n")
    else:
        off.write(line)


off.flush()
off.close()
