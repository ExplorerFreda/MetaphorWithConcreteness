#########################################################################
# File Name: table_mining.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2017-01-10 18:24:22
# Description: This script is used to mine a table, of which columns are
# nouns and rows are adjectives.
#########################################################################

from nltk.corpus import wordnet

dictionary_filenme = '../../data/Corpus/related_data/OxfordDictionary.txt'
concept_net_filename = '../../data/Corpus/related_data/central_by_concept_net.tsv'
type1_pair_filename = '../../data/Corpus/related_data/type-1-pairs.tsv'
type2_pair_filename = '../../data/Corpus/related_data/type-2-pairs.tsv'
output_filename = '../../data/Corpus/related_data/table.tsv'

def load_pairs(filename):
    ret = dict()
    for line in open(filename):
        info = line.split()
        number = int(info[2])
        ret[(info[0],info[1])] = number
    return ret


def combine_pair_info(dict1, dict2):
    for item in dict2:
        if item in dict1:
            dict1[item] += dict2[item]
        else:
            dict1[item] = dict2[item]
    return dict1


def generate_noun_list(pairs):
    count_noun = dict()
    for item in pairs:
        if item[1] not in count_noun:
            count_noun[item[1]] = pairs[item]
        else:
            count_noun[item[1]] += pairs[item]
    count_noun = [(x, count_noun[x]) for x in count_noun]
    count_noun = sorted(count_noun, key = lambda x:-x[1])
    return count_noun[:500]


def generate_adjective_list(nouns, pairs):
    noun_set = set()
    for item in nouns:
        noun_set.add(item[0])
    adjectives = set()
    for item in pairs:
        if item[1] in noun_set:
            adjectives.add(item[0])
    return adjectives


def load_dictionary(filename):
    ret = dict()
    cnt = 0
    for line in open(filename):
        component = line.split('  ')
        if len(component) < 2:
            continue
        word = component[0].lower()
        info = line[len(word) + 2 :].lower().split()
        ret[word] = info
    return ret


def load_conceptnet(filename):
    ret = dict()
    for line in open(filename):
        info = line.split()
        noun = info[2].split('/')
        adj = info[3].split('/')
        if len(noun) < 5 or len(adj) < 5:
            continue
        if noun[4] == 'a' and adj[4] == 'n':
            noun, adj = adj, noun
        if noun[4] != 'n' or adj[4] != 'a':
            continue
        if noun[3] not in ret:
            ret[noun[3]] = []
        ret[noun[3]].append(adj[3])
    return ret


def extract_dictionary(dictionary, adj, noun):
    if noun not in dictionary:
        return 0
    ret = 0
    for item in dictionary[noun]:
        if item == adj:
            ret += 1
    return ret


def extract_conceptnet(conceptnet, adj, noun):
    if noun not in conceptnet:
        return 0
    ret = 0
    for item in conceptnet[noun]:
        if adj == item:
            ret += 1
    return ret


if __name__ == "__main__":
    pairs1 = load_pairs(type1_pair_filename)
    pairs2 = load_pairs(type2_pair_filename)
    pairs = combine_pair_info(pairs1, pairs2)
    nouns = generate_noun_list(pairs)
    adjs = generate_adjective_list(nouns, pairs)
    dictionary = load_dictionary(dictionary_filenme)
    conceptnet = load_conceptnet(concept_net_filename)


    fout = open(output_filename, 'w')
    for item in nouns:
        fout.write('\t\t\t' + item[0])
    fout.write('\n')
    for item in nouns:
        fout.write('\t\t\t' + str(item[1]))
    fout.write('\n')
    for item in nouns:
        fout.write('\tDictionary\tConceptNet\tCorpus')
    fout.write('\n')
    for idx, adj in enumerate(adjs):
        print idx, adj
        fout.write(adj)
        for item in nouns:
            fout.write('\t'+str(extract_dictionary(dictionary, adj, item[0]))+'\t'+str(extract_conceptnet(conceptnet, adj, item[0]))+'\t')
            if (adj,item[0]) in pairs:
                collcation_number = pairs[(adj,item[0])]
            else:
                collcation_number = 0
            fout.write(str(collcation_number))
        fout.write('\n')
    fout.close()