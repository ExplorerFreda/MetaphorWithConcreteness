#########################################################################
# File Name: table_mining_animal.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2017-01-19 15:07:36
# Description: This script is used to mine animal related nouns and their
#   central attributes.
#########################################################################

import table_mining as tm
from nltk.corpus import wordnet as wn


dictionary_filenme = '../../data/Corpus/related_data/OxfordDictionary.txt'
concept_net_filename = '../../data/Corpus/related_data/central_by_concept_net.tsv'
type1_pair_filename = '../../data/Corpus/related_data/type-1-pairs.tsv'
type2_pair_filename = '../../data/Corpus/related_data/type-2-pairs.tsv'
output_filename = '../../data/Corpus/related_data/table_animals.tsv'


def is_animal(synsets):
    if len(synsets) == 0:
        return False
    for item in synsets:
        if item.pos() != 'n':
            continue
        if item in wn.synsets('people') or item in wn.synsets('person') or item in wn.synsets('hominid'):
            continue
        if item == wn.synset('animal.n.01'):
            return True
        if is_animal(item.hypernyms()):
            return True
    return False


def generate_noun_list_animal(pairs):
    count_noun = dict()
    for item in pairs:
        if item[1] not in count_noun:
            count_noun[item[1]] = pairs[item]
        else:
            count_noun[item[1]] += pairs[item]
    count_noun = [(x, count_noun[x]) for x in count_noun]
    count_noun = sorted(count_noun, key=lambda x: -x[1])
    noun_list = list()
    for noun in count_noun:
        if is_animal(wn.synsets(noun[0])):
            noun_list.append(noun)
    print noun_list
    print len(noun_list)
    return noun_list


pairs1 = tm.load_pairs(type1_pair_filename)
pairs2 = tm.load_pairs(type2_pair_filename)
pairs = tm.combine_pair_info(pairs1, pairs2)
nouns = generate_noun_list_animal(pairs)
adjs = tm.generate_adjective_list(nouns, pairs)
dictionary = tm.load_dictionary(dictionary_filenme)
conceptnet = tm.load_conceptnet(concept_net_filename)

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
        fout.write('\t' + str(tm.extract_dictionary(dictionary, adj, item[0])) + '\t' + str(
            tm.extract_conceptnet(conceptnet, adj, item[0])) + '\t')
        if (adj, item[0]) in pairs:
            collcation_number = pairs[(adj, item[0])]
        else:
            collcation_number = 0
        fout.write(str(collcation_number))
    fout.write('\n')
fout.close()