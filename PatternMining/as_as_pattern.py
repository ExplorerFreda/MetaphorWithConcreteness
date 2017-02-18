#########################################################################
# File Name: as_as_pattern.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2017-02-16 05:53:19
# Description: This script is used to mine 'as ... as a/an/nouns' pattern,
# 	for central attribute mining.
#########################################################################

import json

sentence_file_name = '../../data/wikipedia/sentences.txt'
out_filename = '../../data/wikipedia/pattern-mined.txt'
fout = open(out_filename, 'a')


def check(sentence):
	flag = False
	for i in range(len(sentence) - 5):
		if sentence[i] == 'as' and sentence[i+2] == 'as' and  \
			(sentence[i+3] == 'a' or sentence[i+3] == 'an') and \
			(sentence[i+5] == '.' or sentence[i+5]=='!' or sentence[i+5] == ',' or sentence[i+5] == '?' or sentence[i+5] == ';'):
			fout.write(json.dumps(sentence) + '\n')
			print sentence
			print sentence[i+1], sentence[i+4]
			flag = True
	for i in range(len(sentence) - 4):
		if sentence[i] == 'as' and sentence[i+2] == 'as' and  \
			sentence[i+3][-1] == 's' and \
			(sentence[i+4] == '.' or sentence[i+4]=='!' or sentence[i+4] == ',' or sentence[i+4] == '?' or sentence[i+4] == ';'):
			fout.write(json.dumps(sentence) + '\n')
			print sentence
			print sentence[i+1], sentence[i+3]
			flag = True
	return flag


sentence_id = 0
fin = open(sentence_file_name, 'r')
sentences = fin.readlines()
sentences = sentences[sentence_id:-1]
sentence_id += len(sentences)
for idx in range(0,len(sentences)):
	try:
		sentence = json.loads(sentences[idx])
		
		if check(sentence):
			print idx, sentence_id
	except:
		continue
fin.close()
