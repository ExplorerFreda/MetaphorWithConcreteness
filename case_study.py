import load_wordlist

'''
pairs
room	furnace
love	rose
life	journey
society	organism
teacher	lamp
elephant	wall
idea	cell
corruption	mudslide
creativity	muscle
death	mirror
'''

whole_wordlist_filename = '../data/adj+n_simp.tsv'
pair_filename = '../data/pairs.tsv'


def load_case_pair(filename):
    ret = []
    for item in open(filename):
        [target, source] = item[:-1].split('\t')
        ret.append((target, source))
    return ret


pairs = load_case_pair(pair_filename)
set_of_pairs = set()
for item in pairs:
    set_of_pairs.add(item[0])
    set_of_pairs.add(item[1])
print len(set_of_pairs)
wordlist = load_wordlist.load_wordlist(whole_wordlist_filename)
noun_adj = dict()
for item in wordlist:
    if item[1] in set_of_pairs:
        if not noun_adj.has_key(item[1]):
            noun_adj[item[1]] = []
        noun_adj[item[1]].append((item[0], item[2]))

output_filename = '../data/case_study.tsv'
fout = open(output_filename, 'w')
for item in pairs:
    for subitem in noun_adj[item[0]]:
        fout.write(subitem[0] + '\t' + item[0] + '\t' + str(subitem[1]) + '\n')
    fout.write('# ' + item[1] + '\n')
    for subitem in noun_adj[item[1]]:
        fout.write(subitem[0] + '\t' + item[1] + '\t' + str(subitem[1]) + '\n')
fout.close()
