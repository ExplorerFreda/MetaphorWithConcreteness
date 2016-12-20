import load_wordlist


output_filename = '../../data/Corpus/related_data/adj+n_simp_analysis.tsv'
wordlist = load_wordlist.load_wordlist('../../data/Corpus/related_data/adj+n_simp.tsv', False)
concreteness = load_wordlist.load_concreteness('../../data/duplication/concreteness_score_dup_pearson.txt')

fout = open(output_filename, 'w')
for (iter, item) in enumerate(wordlist):
    left = item[0]
    right = item[1]
    cnt = item[2]
    if left not in concreteness or right not in concreteness or cnt < 20:
        continue
    fout.write(left + '\t' + str(concreteness[left]) + '\t' + right + '\t' + str(concreteness[right]) + '\t' +
               str(cnt) + '\n')
    print iter
fout.close()