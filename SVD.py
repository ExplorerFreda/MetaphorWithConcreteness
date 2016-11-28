from scipy.sparse import linalg as sl
from scipy.sparse import coo_matrix
import numpy as np
import math
import json

dictionary = open('../../data/duplication/dictionary.txt').readlines()
Dict = dict()
WordCount = dict()
c1 = 0
index = -1
for item in dictionary:
    [word, cnt] = item.split('\t')
    cnt = int(cnt)
    if cnt >= 50:
        index += 1
        Dict[word] = index
        WordCount[index] = cnt
        c1 += cnt
wc = len(Dict)
print 'Total Word Count:', c1
print 'Word Count:', wc

row = []
col = []
data = []
for item in open('../../data/duplication/matrix.txt'):
    [LeftIndex, RightIndex, Count] = item.split('\t')
    LeftIndex = int(LeftIndex)
    RightIndex = int(RightIndex)
    Count = int(Count)
    ppmi = math.log(c1) + math.log(Count) - math.log(WordCount[LeftIndex]) - math.log(WordCount[RightIndex])
    if ppmi > 0:
        row.append(LeftIndex)
        col.append(RightIndex)
        data.append(ppmi)
        row.append(RightIndex)
        col.append(LeftIndex + wc)
        data.append(ppmi)

'''
data = [1,2,3,4]
row = [1,2,3,4]
col = [1,2,3,4]
wc = 11
'''

print 'SVD procedure begins.'
A = coo_matrix((data, (row, col)), shape = (wc, wc + wc), dtype = np.float)
[u, sigma, v] = sl.svds(A, k = 1000)
print 'SVD procedure done.'

foutu = open('../../data/duplication/u.txt', 'w')
for line in u:
    foutu.write(json.dumps(line.tolist()) + '\n')
foutu.close()

fouts = open('../../data/duplication/sigma.txt', 'w')
fouts.write(json.dumps(sigma.tolist()) + '\n')
fouts.close()

foutv = open('../../data/duplication/v.txt', 'w')
for line in v:
    foutv.write(json.dumps(line.tolist()) + '\n')
foutv.close()