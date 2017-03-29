from nltk.corpus import wordnet as wn
import json

def English(word):
    flag = False
    for c in word:
        if ('a' <= c <= 'z') or ('A' <= c <= 'Z'):
            flag = True
            break
    return flag and len(wn.synsets(word)) != 0


def load_wordlist(filename, with_checking=True):
    ret = []
    curr_progress = 0
    for line in open(filename):
        curr_progress += 1
        if curr_progress % 10000 == 0:
            print 'loading wordlist: ', curr_progress
        [word_l, word_r,  cnt] = line.split('\t')
        if with_checking and (not English(word_l) or not English(word_r)):
            continue
        cnt = int(cnt)
        ret.append((word_l, word_r, cnt))
    if with_checking:
        ret = sorted(ret, key=lambda x:(x[0],-x[2]))
    return ret


def load_concreteness(filename):
    ret = dict()
    for line in open(filename):
        [word, conc] = line.split('\t')
        conc = float(conc)
        ret[word] = conc
    return ret

'''
wordlist = load_wordlist('../../data/Corpus/related_data/adj+n.tsv')
print len(wordlist)
fout = open('../../data/Corpus/related_data/adj+n_simp.tsv', 'w')
for triple in wordlist:
    fout.write(triple[0] + '\t' + triple[1] + '\t' + str(triple[2]) +'\n')
fout.close()
'''