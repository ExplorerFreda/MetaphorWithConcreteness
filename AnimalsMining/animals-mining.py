#########################################################################
# File Name: animals-mining.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2017-02-20 22:53:03
# Description: This script is used to mine animals from a list of nouns.
#########################################################################

import json
import urllib
from nltk.corpus import wordnet as wn

word_list_filename = '../../data/bnc/NN.txt'
animals_filename = '../../data/bnc/animals_noun.txt'
linggle_query_url = 'http://linggle.com/query/'


fout = open(animals_filename, 'w')


def HasHypernym(word, synset):
	if type(word) == type(u'string'):
		word = wn.synsets(word)
	for w in word:
		if w == synset:
			return True
		if HasHypernym(w.hypernyms(), synset):
			return True
	return False


def Check(word):
	if not HasHypernym(word, wn.synset('animal.n.01')):
		return False
	query = linggle_query_url + word + ' is an animal/insect'
	if len(json.loads(urllib.urlopen(query).read())) > 0:
		return True
	return False




if __name__ == '__main__':
	cnt = 0
	for idx, line in enumerate(open(word_list_filename)):
		data = json.loads(line)
		if Check(data[0]):
			cnt += 1
			print data, cnt 
			fout.write(data[0] + '\n')
		if idx % 10000 == 0:
			print idx

	fout.close()
