#########################################################################
# File Name: as_as_pairs_from_linggle_result.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2017-02-18 22:03:35
# Description: This script is used to extract all pairs extracted from 
#	linggle.com.
#########################################################################

import json

input_filename = '../../data/bnc/as-as-pattern-by-JJ.txt'
fout_filename = '../../data/bnc/as-as-pairs-by-JJ.txt'

fout = open(fout_filename, 'w')

def CheckPhrase1(phrase): #as ADJ as a/an NOUN
	if len(phrase) != 5:
		return False
	if phrase[0] != 'as' or phrase[2] != 'as' or (phrase[3] != 'a' and phrase[3] != 'an'):
		return False
	return True


pair_set = set()
for line in open(input_filename):
	data = json.loads(line)
	for item in data:
		phrase = item['phrase']
		count = item['count']
		percent = item['percent']
		if not CheckPhrase1(phrase):
			continue
		adj = phrase[1]
		noun = phrase[-1]
		pair_set.add((adj, noun, count, percent))
pair_list = sorted(pair_set, key=lambda x:x[0])
for item in pair_list:
	output_item = dict()
	output_item['adj'] = item[0]
	output_item['noun'] = item[1]
	output_item['count'] = item[2]
	output_item['percent'] = item[3]
	fout.write(json.dumps(output_item) + '\n')

fout.close()
