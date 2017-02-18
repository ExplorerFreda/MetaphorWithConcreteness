#########################################################################
# File Name: PMI-computing.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2017-02-09 21:21:02
# Description: This script is used to compute PMI
#########################################################################

import numpy as np
import json
import math

config = 's'
corpus_filename = '../data/sentences_withpostag.tsv'

def PrintPercentage(idx, total):
	if int(float(idx+2)/(total+1)*100) > int(float(idx+1)/(total+1)*100):
		print 'processed', str(int(float(idx+2)/(total+1)*100))+'%,', (idx+1), 'files'


def Save(data, filename):
	fout = open(filename, 'w')
	fout.write(json.dumps(data) + '\n')
	fout.close()


def Load(filename):
	return json.loads(open(filename).readline())


def CountWordsAndPairs(corpus):
	ret_words = dict()
	ret_pairs = dict()
	C1 = 0
	for idc, line in enumerate(corpus):
		words = line.lower().split('\t')[0].split()
		postags = line.split('\t')[1].split()
		last_word = '!@#$%^&*()'
		for idx, word in enumerate(words):
			if word not in ret_words:
				ret_words[word] = 1
			else:
				ret_words[word] += 1 # words counts
			if last_word == '!@#$%^&*()':
				last_word = word
				continue
			else:
				if postags[idx-1] != 'JJ' or postags[idx][:2] != 'NN':
					last_word = word
					continue
				if last_word+'~-~'+word not in ret_pairs:
					ret_pairs[last_word+'~-~'+word] = 1
				else:
					ret_pairs[last_word+'~-~'+word] += 1
				last_word = word
		C1 += len(words)
		PrintPercentage(idc,len(corpus))
	return ret_words, ret_pairs, C1


def MakePairs(pair_count, with_special_noun, special_noun_set):
	ret = set()
	if not with_special_noun:
		for item in pair_count:
			ret.add(tuple(item.split('~-~')))
	else:
		for item in pair_count:
			if item.split('~-~')[1] in special_noun_set:
				ret.add(tuple(item.split('~-~')))
	return ret

# save
if config == 's':
	corpus = open(corpus_filename).readlines()
	word_count, pair_count, C1 = CountWordsAndPairs(corpus)
	Save(word_count, '../data/temp/word_count.txt')
	Save(pair_count, '../data/temp/pair_count.txt')
	print len(word_count), len(pair_count), C1
elif config == 'l':
	C1 = 100620105 # computed by this script 
	word_count = Load('../data/temp/word_count.txt')
	pair_count = Load('../data/temp/pair_count.txt')
	print len(word_count), len(pair_count), C1

special_animal_nouns = ['fish','dog','bird','horse','cat','sheep','cattle','insect','cow','mouse','chicken','tiger ','rabbit','snake','frog']
pair_set = MakePairs(pair_count, with_special_noun = True, special_noun_set = set(special_animal_nouns))

pmi_list = dict()
for item in pair_set:
	left_word = item[0]
	right_word = item[1]
	if word_count[left_word] < 20:
		continue
	pmi = math.log(C1) + math.log(pair_count[left_word+'~-~'+right_word]) - math.log(word_count[left_word]) - math.log(word_count[right_word])
	if right_word not in pmi_list:
		pmi_list[right_word] = dict()
	pmi_list[right_word][left_word] = pmi


fout = open('../data/pmi_case_study.tsv', 'w')
for item in pmi_list:
	pmi_list_left = pmi_list[item]
	pmi_list_left = [(x, pmi_list_left[x]) for x in pmi_list_left]
	pmi_list_left = sorted(pmi_list_left, key = lambda x:-x[1])
	for sub_item in pmi_list_left:
		fout.write(sub_item[0] + ' ' + item + ' ' + str(sub_item[1]) + '\n')
fout.close()

