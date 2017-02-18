#########################################################################
# File Name: pos-mining.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2017-02-18 07:55:26
# Description: This script is used to mine the frequency of certain POS Tag.
#########################################################################

import json


input_filename = '../../data/bnc/sentences_withpostag.tsv'
tag_prefix = 'JJ'
output_filename = input_filename[:input_filename.rfind('/')+1]+tag_prefix+'.txt'
fout = open(output_filename,'w')


freq_dict = dict()
for idx, line in enumerate(open(input_filename)):
	data = line.split('\t')
	words = data[0].split()
	postags = data[1].split()
	for i in xrange(len(words)):
		if postags[i][:len(tag_prefix)] == tag_prefix:
			if words[i] in freq_dict:
				freq_dict[words[i]] += 1
			else:
				freq_dict[words[i]] = 1
	if idx % 10000 == 0:
		print idx

freq_list = sorted([(x,freq_dict[x]) for x in freq_dict], key = lambda x:-x[1])
for item in freq_list:
	fout.write(json.dumps(item) + '\n')
fout.close()
