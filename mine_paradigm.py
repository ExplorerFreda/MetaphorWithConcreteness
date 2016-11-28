#########################################################################
# File Name: mine_paradigm.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2016-08-26 16:40:43
# Description: This script is used to mine paradigm in the duplication of concreteness experiment.
#########################################################################

model_name = 'senna'
correlation_name = 'pearson'
print model_name, correlation_name

import spearman
import pearson
import numpy as np

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
    elif conf == 'senna':
        dictionary = open('../../data/senna/dictionary.txt').readlines()
        Dict = dict()
        index = -1
        for item in dictionary:
            index += 1
            Dict[item[:-1]] = index
    return Dict
def load_vector(conf, mrc_dict, Dict):
    mrc_dict = sorted([(x, Dict[x]) for x in mrc_dict], key=lambda x:x[1])
    ret = dict()
    if conf == 'huang':
        filename = '../../data/Huang et al/wordVectors.txt'
    elif conf == 'dup':
        filename = '../../data/duplication/wordVectors.txt'
    elif conf == 'senna':
        filename = '../../data/senna/embeddings.txt'
    pointer = 0
    for idx,line in enumerate(open(filename).readlines()):
        if pointer < len(mrc_dict) and mrc_dict[pointer][1] == idx:
            ret[mrc_dict[pointer][0]] = np.array([float(x) for x in line.split()])
            pointer += 1
    return ret
def cosine(x, y):
    return np.sum(x*y)/np.sum(x*x)**0.5/np.sum(y*y)**0.5

Dict = load_dictionary(model_name)
wc = len(Dict)
print 'Word Count:', wc

# load MRC dictionary
mrc_dict = dict()
mini = 10000
maxi = 0
for line in open('../../data/MRC/1054/mrc2.dct'):
    conc = int(line[28:31])
    word = line[51:line.find('|')].lower()
    if word not in Dict:
        continue
    if conc != 0:
        mrc_dict[word] = conc

mrc_vectors = load_vector(model_name, mrc_dict, Dict)
print 'Word# in MRC dict:', len(mrc_dict)
print 'Word# in loaded vector:', len(mrc_vectors)

# Mine paradigms
train_words = list()
test_words = list()
for word in mrc_dict:
    if len(train_words) > len(test_words):
        test_words.append(word)
    else:
        train_words.append(word)
print 'Word# for training and testing:', len(train_words), len(test_words)

conc_score = dict()
paradigms = dict()
for word in train_words:
    conc_score[word] = 0
step = 0
while True:
    if step % 2 == 0:  # mine positive
        positive = 1
    else:
        positive = -1
    selected_new_conc_score = dict()
    selected_new_correlation = -1
    selected_new_paradigm_word = ''
    for word in train_words:
        if word in paradigms:
            continue
        new_conc_score = dict()
        for update_word in train_words:
            new_conc_score[update_word] = conc_score[update_word] + \
                                          positive * cosine(mrc_vectors[word], mrc_vectors[update_word])
        if correlation_name == 'spearman':
            correlation = spearman.spearman(new_conc_score, mrc_dict)
        elif correlation_name == 'pearson':
            correlation = pearson.pearson(new_conc_score, mrc_dict)
        if correlation > selected_new_correlation:
            selected_new_paradigm_word = word
            selected_new_correlation = correlation
            selected_new_conc_score = new_conc_score.copy()
    conc_score = selected_new_conc_score.copy()
    paradigms[selected_new_paradigm_word] = positive
    print 'Step', step, ',', correlation_name, 'correlation:', selected_new_correlation
    test_conc_score = dict()
    for word in test_words:
        test_conc_score[word] = 0
        for paradigm in paradigms:
            test_conc_score[word] += paradigms[paradigm] * cosine(mrc_vectors[paradigm], mrc_vectors[word])
    if correlation_name == 'spearman':
        print '\tTest Spearman correlation:', spearman.spearman(test_conc_score, mrc_dict)
    elif correlation_name == 'pearson':
        print '\tTest Pearson correlation:', pearson.pearson(test_conc_score, mrc_dict)
    print '\tParadigms:', paradigms
    step += 1
    if step > 100:
        break