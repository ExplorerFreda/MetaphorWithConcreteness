import load_wordlist

LOCAL = 1

if LOCAL:
    output_filename = '../data/adj+n_simp_analysis.tsv'
    output_filename_byadj = '../data/adj+n_simp_analysis_adj.tsv'
    wordlist = load_wordlist.load_wordlist('../data/adj+n_simp.tsv', False)
    concreteness = load_wordlist.load_concreteness('../data/concreteness_score_dup_pearson.txt')
else:
    output_filename = '../../data/Corpus/related_data/adj+n_simp_analysis.tsv'
    output_filename_byadj = '../../data/Corpus/related_data/adj+n_simp_analysis_adj.tsv'
    wordlist = load_wordlist.load_wordlist('../../data/Corpus/related_data/adj+n_simp.tsv', False)
    concreteness = load_wordlist.load_concreteness('../../data/duplication/concreteness_score_dup_pearson.txt')


def English(word):
    for c in word:
        if c > 'z' or c < 'a':
            return False
    return True


dataset = list()
fout = open(output_filename, 'w')
for (iteration, item) in enumerate(wordlist):
    left = item[0]
    right = item[1]
    cnt = item[2]
    if left not in concreteness or right not in concreteness:
        continue
    if not English(left) or not English(right):
        continue
    line = left + '\t' + right + '\t' + str(cnt) + '\t'\
           + str(concreteness[left]) + '\t' + str(concreteness[right]) + '\n'
    fout.write(line)
    dataset.append([line, left, cnt])
    if iteration % 10000 == 0:
        print iteration
fout.close()

fout = open(output_filename_byadj, 'w')
dataset = sorted(dataset, key=lambda x:(x[1],- x[2]))
for item in dataset:
    fout.write(item[0])
fout.close()