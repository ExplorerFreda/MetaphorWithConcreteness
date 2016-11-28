#########################################################################
# File Name: generate_all_concreteness.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2016-08-26 16:40:43
# Description: This script is used to generate the conccreteness of all
#   words in the given dictionary.
#########################################################################
model_name = 'dup'
correlation_name = 'pearson'
print model_name, correlation_name

import numpy as np
import json

def load_dictionary(conf):
    if conf == 'dup':
        dictionary = open('../../data/duplication/dictionary.txt').readlines()
        Dict = dict()
        index = -1
        for item in dictionary:
            [word, cnt] = item.split('\t')
            cnt = int(cnt)
            if cnt >= 50:
                index += 1
                Dict[word] = index
    elif conf == 'huang':
        dictionary = open('../../data/Huang et al/vocab.txt').readlines()
        Dict = dict()
        index = -1
        for item in dictionary:
            index += 1
            Dict[item[:-1]] = index
    return Dict
def load_vector(conf, Dict):
    sorted_dict = sorted([[x, Dict[x]] for x in Dict], key=lambda x:x[1])
    ret = dict()
    if conf == 'huang':
        filename = '../../data/Huang et al/wordVectors.txt'
    elif conf == 'dup':
        filename = '../../data/duplication/wordVectors.txt'
    pointer = 0
    for idx,line in enumerate(open(filename).readlines()):
        if pointer < len(sorted_dict) and sorted_dict[pointer][1] == idx:
            ret[sorted_dict[pointer][0]] = np.array([float(x) for x in line.split()])
            pointer += 1
    return ret
def load_paradigm(info):
    return json.loads(raw_input(info).replace("'", '"'))
def cosine(x, y):
    return np.sum(x*y)/np.sum(x*x)**0.5/np.sum(y*y)**0.5

Dict = load_dictionary(model_name)
vectors = load_vector(model_name, Dict)
paradigms = load_paradigm('Please input the paradigms:')
print len(Dict), len(vectors), len(paradigms)
output_filename = '../../data/duplication/concreteness_score_' + model_name + '_' + correlation_name + '.txt'


concreteness_score = dict()
for word in vectors:
    concreteness_score[word] = 0
fout = open(output_filename, 'w')
for paradigm in paradigms:
    for word in concreteness_score:
        concreteness_score[word] += paradigms[paradigm] * cosine(vectors[word], vectors[paradigm])
concreteness_score = sorted([[d,concreteness_score[d]] for d in concreteness_score], key=lambda x:x[1], reverse=True)
for item in concreteness_score:
    fout.write(item[0] + '\t' + str(item[1]) + '\n')
fout.close()
