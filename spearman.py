#########################################################################
# File Name: spearman.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2016-08-26 16:40:43
# Description: This script is used to compute Spearman Correlation.
#########################################################################

def rank(x):
    sa = []
    ret = [0 for i in range(len(x))]
    for i in range(len(x)):
        sa.append([i,x[i]])
    sa = sorted(sa, key = lambda x:x[1])
    i = 0
    while i < len(sa):
        j = i
        while j < len(sa) and sa[i][1] == sa[j][1]:
            j += 1
        ret[sa[i][0]] = i
        for k in range(i, j):
            ret[sa[k][0]] = float(i+j-1)/2
        i = j
    return ret


def clear(X,Y):
    retx = []
    rety = []
    for d in X:
        if d in Y:
            retx.append(X[d])
            rety.append(Y[d])
    return [retx, rety]


def spearman(X,Y):
    [X,Y] = clear(X,Y)
    X = rank(X)
    Y = rank(Y)
    n = len(X)
    ret = 0
    for i in range(n):
        ret += 6.0 * ((X[i]-Y[i])**2)
    ret = 1 - ret / n / (n-1) / (n+1)
    return ret

