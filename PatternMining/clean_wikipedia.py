#########################################################################
# File Name: clean_wikipedia.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2017-02-15 07:07:55
# Description: This script is used to clean wikipedia language source.
#########################################################################

from bs4 import BeautifulSoup
import nltk
import json
import codecs

homeDir = '../../data/wikipedia/'
htmlList = 'html.lst'

# get total file number
totalFiles = len(open(homeDir + htmlList).readlines())
print totalFiles


for idx, line in enumerate(open(homeDir + htmlList, 'r')):
	if idx < 6813781: # the number is the last fail document
		continue
	# open output file each time
	fout = open(homeDir + 'sentences.txt', 'a')
	print '%d files of %d processed'%(idx+1, totalFiles), line.strip()
	html_doc = open(homeDir + line.strip()).read()
	soup = BeautifulSoup(html_doc, 'html.parser')
	text = soup.get_text()
	sentences = nltk.sent_tokenize(text)
	for sentence in sentences:
		words = nltk.word_tokenize(sentence)
#		tags = nltk.pos_tag(nltk.word_tokenize(sentence))
#		words = map(lambda x:x[0], tags)
#		tags = map(lambda x:x[1], tags)
		fout.write(json.dumps(words) + '\n')
#		fout.write(json.dumps(tags) + '\n')
	
	fout.close()
