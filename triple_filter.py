triple_filename = '../../data/EACLData/triple_2_INF.tsv'
output_filename = '../../data/EACLData/triple_filtered.tsv'
concept_dict_filename = '../../data/EACLData/concept_dict.tsv'
data = []
target_count = dict()
concept_dict = set()
fout = open(output_filename, 'w')
for line in open(triple_filename):
    row = line[:-1].split('\t')
    if row[2] != 'H':
        fout.write(line)
        concept_dict.add(row[0])
        concept_dict.add(row[1])
        continue
    data.append(row)
    if row[0] not in target_count:
        target_count[row[0]] = 0
    target_count[row[0]] += int(row[3])

last_index = 0
for i in range(1, len(data)):
    if data[i][0] != data[i-1][0] or i == len(data)-1:
        subdata = []
        sum_count = 0
        curr_count = 0
        for j in range(last_index, i):
            subdata.append(data[j])
            sum_count += int(data[j][3])
        last_index = i
        subdata.reverse()
        for item in subdata:
            curr_count += int(item[3])
            concept_dict.add(item[0])
            concept_dict.add(item[1])
            fout.write(item[0]+'\t'+item[1]+'\t'+item[2]+'\t'+item[3]+'\n')
            if curr_count > sum_count * 0.6:
                break
fout.close()


fout = open(concept_dict_filename, 'w')
for item in concept_dict:
    fout.write(item+'\n')
fout.close()