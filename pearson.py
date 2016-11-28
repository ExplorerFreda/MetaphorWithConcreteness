#########################################################################
# File Name: pearson.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2016-11-21 16:49:59
# Description: This script is used to compute Pearson Correlation.
#########################################################################
import numpy as np

def clear(X,Y):
    retx = []
    rety = []
    for d in X:
        if d in Y:
            retx.append(X[d])
            rety.append(Y[d])
    return [np.array(retx), np.array(rety)]


def pearson(X,Y):
    [X, Y] = clear(X, Y)
    X = X - np.average(X)
    Y = Y - np.average(Y)
    return np.sum(X*Y)/np.sum(X*X)**0.5/np.sum(Y*Y)**0.5
