import sys

iori2delos = sys.argv[1]
idelos2ori = sys.argv[2]

best_ori2delos_item = dict()
best_ori2delos_score = dict()
for line in open(iori2delos,'r'):
    cc = line.split('\t')
    if (cc[0] not in best_ori2delos_item) or (float(cc[11]) < best_ori2delos_score[cc[0]]):
        best_ori2delos_item[cc[0]] = cc[1]
        best_ori2delos_score[cc[0]] = float(cc[11])


best_delos2ori_item = dict()
best_delos2ori_score = dict()
for line in open(idelos2ori,'r'):
    cc = line.split('\t')
    if (cc[0] not in best_delos2ori_item) or (float(cc[11]) < best_delos2ori_score[cc[0]]):
        best_delos2ori_item[cc[0]] = cc[1]
        best_delos2ori_score[cc[0]] = float(cc[11])


for k,v in best_ori2delos_item.items():
    if (v in best_delos2ori_item) and (k == best_delos2ori_item[v]):
        print(k,v)
