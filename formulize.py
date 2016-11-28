#########################################################################
# File Name: formulize.py
# Author: Haoyue Shi
# mail: freda.haoyue.shi@gmail.com
# Created Time: 2016-08-26 16:40:43
# Description: This script is used to formulize the table which is need to shown.
#########################################################################
import json

for i in range(3):
    line = raw_input()
output = []
dic = dict()
while True:
    output_line = ''
    for i in range(2):
        line = raw_input().split()
        if len(line) == 0 or line[0] != 'Step':
            for line in output:
                print line
            exit()
        step = int(line[1]) + 1
        correlation = float(line[-1])
        raw_input()
        line = raw_input()[12:]
        line = line.replace("'",'"')
        print line
        new_dict = json.loads(line)
        output_line += str(step) + '\t'
        for item in new_dict:
            if item not in dic:
                output_line += item + '\t'
        output_line += str(correlation) + '\t'
        dic = new_dict.copy()
    output.append(output_line)
