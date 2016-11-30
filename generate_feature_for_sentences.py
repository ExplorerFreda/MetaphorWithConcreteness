data_type = 'TroFi'
import json


def load_sentences(filename, data_type):
    fin = open(filename)
    if data_type == 'TroFi':
        ret = dict()
        for line in fin:
            if line[:3] == '***' and line[:4] != '****':
                word = line[3:]
                word = word[:word.find('*')]
                ret[word] = list()
            elif line[0] == '*' or len(line) < 2:
                continue
            else:
                items = line.split('\t')
                sent = items[2]
                postag = items[3]
                lemmatization = items[4]
                tag = items[1]
                ret[word].append((sent, postag, lemmatization,tag))
    else:
        ret = dict()
    fin.close()
    return ret
def load_conc_dict(filename):
    ret = dict()
    maxi = -10
    mini = 10
    for line in open(filename):
        ret[line.split()[0]] = float(line.split()[1])
        maxi = max(maxi, float(line.split()[1]))
        mini = min(mini, float(line.split()[1]))
    for key in ret:
        ret[key] = (ret[key] - mini) / (maxi - mini)
    return ret
def compute_avg_concreteness(sentence, postag, prefix, concreteness, except_verb = 'NONE'):
    res = 0
    cnt = 0
    for i in range(len(postag)):
        if postag[i][:len(prefix)] == prefix and (sentence[i] in concreteness) and sentence[i] != except_verb:
            cnt += 1
            res += concreteness[sentence[i]]
    if cnt == 0:
        return 0.5
    return res / cnt

data = load_sentences('../../data/TroFi/TroFiTokenized.txt', data_type)
conc_dict = load_conc_dict('../../data/duplication/concreteness_score_dup_pearson.txt')
feature = dict()
fout = open('../../data/duplication/feature.txt', 'w')
for word in data:
    fout.write(word + '\n')
    for item in data[word]:
        sentence = item[2].split()
        postag = item[1].split()
        conc_noun = compute_avg_concreteness(sentence, postag, 'NN', conc_dict)
        conc_prep = compute_avg_concreteness(sentence, postag, 'PRP', conc_dict)
        conc_verb = compute_avg_concreteness(sentence, postag, 'VB', conc_dict, word)
        conc_adj =  compute_avg_concreteness(sentence, postag, 'JJ', conc_dict)
        conc_adv =  compute_avg_concreteness(sentence, postag, 'RB', conc_dict)
        print conc_noun, conc_prep, conc_verb, conc_adj, conc_adv, item[3]
        fout.write(str(conc_noun) + ' ' + str(conc_prep) + ' ' + str(conc_verb) + ' ' + str(conc_adj) + ' ' + str(conc_adv)
                   + ' ' + item[3] + '\n')
    fout.write('\n')
fout.close()
