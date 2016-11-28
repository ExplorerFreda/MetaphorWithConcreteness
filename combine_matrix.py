# This script is used to generate X Matrix by Frequency Matrix
import math

dictionary = open('../../data/duplication/dictionary.txt').readlines()
Dict = dict()
WordCount = dict()
c1 = 0
index = 0
for item in dictionary:
    [word, cnt] = item.split('\t')
    cnt = int(cnt)
    if cnt >= 50:
        index += 1
        Dict[word] = index
        WordCount[index] = cnt
        c1 += cnt
print 'Total Word Count:', c1
print 'Word Count:', len(Dict)

x = dict()
fout = open('../../data/duplication/ppmi_matrix_left.txt', 'w')
LastIndex = 1
for item in open('../../data/duplication/matrix_left.txt'):
    [LeftIndex, RightIndex, Count] = item.split('\t')
    LeftIndex = int(LeftIndex) + 1
    RightIndex = int(RightIndex) + 1
    Count = int(Count)
    ppmi = math.log(c1) + math.log(Count) - math.log(WordCount[LeftIndex]) - math.log(WordCount[RightIndex])
    if ppmi > 0:
        x[RightIndex] = ppmi
    while LastIndex < LeftIndex:
        print LastIndex, len(x)
        for j in range(1, len(Dict) + 1):
            if j in x:
                fout.write(' ' + str(j) + ':' + str(x[j]))
        fout.write('\n')
        x = dict()
        LastIndex += 1

while LastIndex <= len(Dict):
    print LastIndex, len(x)
    for j in range(1, len(Dict) + 1):
        if j in x:
            fout.write(' ' + str(j) + ':' + str(x[j]))
    fout.write('\n')
    x = dict()
    LastIndex += 1

fout.close()