#########################################################################
# File Name: as_as_pattern_from_linggle.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2017-02-18 08:45:26
# Description: This script is used to mine 'as ... as' pattern from linggle.com
#########################################################################

import urllib2
import urllib
import json

# a/an pattern
url = 'http://linggle.com/query/as %s as a/an n.'
adj_list_filename = '../../data/bnc/JJ.txt'
output_filename = '../../data/bnc/as-as-pattern-by-JJ.txt'
fout = open(output_filename, 'a')

for idx, line in enumerate(open(adj_list_filename)):
	try:
		item = json.loads(line)
		query = url%item[0]
		data = json.loads(urllib.urlopen(query).read())
		fout.write(json.dumps(data) + '\n')
		print idx, line, data
	except:
		break
fout.close()
