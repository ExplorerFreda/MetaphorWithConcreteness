import codecs

relation_set = set()
fout = codecs.open('../../data/Corpus/related_data/central_by_concept_net.tsv', 'w', encoding='utf8')
for i in range(8):
    filename = '../../data/ConceptNet/assertions/part_0%d.csv'%i
    print filename
    for line in codecs.open(filename, encoding='utf8'):
        items = line.split('\t')
        relation_set.add(items[1])
        if items[1] == '/r/HasProperty' or items[1] == '/r/wordnet/adjectivePertainsTo' or items[1] == '/r/Attribute':
            fout.write(line)
fout.close()