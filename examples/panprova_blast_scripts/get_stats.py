import sys

imap = sys.argv[1] #'blast_all'
ipanprova = sys.argv[2] #'10_genomes.gene_families'
ipandelos = sys.argv[3] #'output.clus'

print('reading mapping...')
prgenes = set()
degenes = set()

pr2de = dict()
de2pr = dict()

for line in open(imap,'r'):
    cc = line.strip().split(' ')
    de = cc[1]
    pr = cc[0]
    
    degenes.add(de)
    prgenes.add(pr)

    if de not in de2pr:
        de2pr[de] = pr
    if pr not in pr2de:
        pr2de[pr] = de


print('panprova (pr) genes', len(prgenes), ';pandelos (de) genes', len(degenes))
print('pr mappings',len(pr2de), ';de mappings', len(de2pr))

print()
print('reading panprova homologies...')
prgenes = set()
prhomos = set()
for line in open(ipanprova,'r'):
    cc = line.strip().split(' ')
    for i in range(1, len(cc)):
        prgenes.add(cc[i])
        for j in range(i+1, len(cc)):
            prhomos.add( (cc[i],cc[j]) )
            prhomos.add( (cc[j],cc[i]) )
print('involved pr genes', len(prgenes),';number of homologies', len(prhomos))

print()
print('reading pandelos homologies...')
dehomos = set()
degenes = set()
for line in open(ipandelos,'r'):
    cc = line.strip().split(' ')
    for i in range(0, len(cc)):
        degenes.add(cc[i])
        for j in range(i+1, len(cc)):
            dehomos.add( (cc[i],cc[j]) )
            dehomos.add( (cc[j],cc[i]) )
print('involved de genes', len(degenes), ';number of homologies', len(dehomos))


print()
print('getting statistics...')
tp,tn,fp,fn = 0,0,0,0

for c in dehomos:
    if (c[0] in de2pr) and (c[1] in de2pr):
        m = ( de2pr[c[0]], de2pr[c[1]] )
        if m in prhomos:
            tp += 1
        else:
            fp += 1

for c in prhomos:
    if (c[0] in pr2de) and (c[1] in pr2de):
        m = ( pr2de[c[0]], pr2de[c[1]] )
        if m not in dehomos:
            fn += 1

print('tp',tp,'fp',fp,'fn',fn)
precision = tp/ ( tp +fp )
recall = tp / (tp + fn)
f1score = 2 * tp / ( (2*tp) + fp + fn )
fdr = fp / (fp + tp)

print('preicsion',precision,'recall', recall,'f1score',f1score,'fdr',fdr)

