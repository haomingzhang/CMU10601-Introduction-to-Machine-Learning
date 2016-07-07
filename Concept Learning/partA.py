#!/usr/bin/python
import sys
import math

#train
trainfile = open('9Cat-Train.labeled', 'r')
output = open('partA4.txt', 'w')
pos = 'high'
neg = 'low'
h = {}
keys = []
count = 0;
for line in trainfile:
	words = line.split('\t')
	if count == 0:
		#input space
		print 2**(len(words) - 1)
		#number of digets of size of concept space
		print int(math.log(2**(2**(len(words)-1)),10)) + 1
		#hypothesis space
		print 3**(len(words) - 1) + 1
		for word in words[:-1]:
			keys.append(word.split()[0])

	if words[-1].split()[1] == pos:
		for i in range(len(words) - 1):
			att, val = words[i].split()
			if not h.has_key(att):
				h[att] = val

			elif (h[att] != '?') and (h[att] != val):
				h[att] = '?'
	count += 1
	if count%30 == 0:
		string = ''
		for key in keys:
			string += h[key] + '\t'
		print >> output, string[:-1]
	
trainfile.close()
#test on 9Cat-Dev.labeled
testfile = open('9Cat-Dev.labeled', 'r')
right = 0.0
wrong = 0.0
for line in testfile:
	words = line.split('\t')
	flag = True
	for i in range(len(words) - 1):
		att, val = words[i].split()
		if h[att] != '?' and h[att] != val:
			flag = False
	if (flag and words[-1].split()[1] == pos) or ((not flag) and  words[-1].split()[1] != pos):
		right += 1
	else:
		wrong += 1

print wrong/(right+wrong)

testfile.close()
#input
inputfile = open(sys.argv[1], 'r')
for line in inputfile:
	words = line.split('\t')
	flag = True
	for word in words:
		#print word
		att, val = word.split()
		if h.has_key(att) and h[att] != '?' and h[att] != val:
			flag = False
	if flag:
		print pos
	else:
		print neg

inputfile.close()


