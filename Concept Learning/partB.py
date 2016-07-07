#!/usr/bin/python
import sys
import math

#train
trainfile = open('4Cat-Train.labeled', 'r')
pos = 'high'
neg = 'low'

#input space
print 2**4
#concept space
print 2**(2**4)

posSet = set()
negSet = set()

for line in trainfile:
	words = line.split('\t')
	tmp = 0
	tmp += (words[0].split()[1] == 'Male') << 0;
	tmp += (words[1].split()[1] == 'Young') << 1;
	tmp += (words[2].split()[1] == 'Yes') << 2;
	tmp += (words[3].split()[1] == 'Yes') << 3;
	if words[-1].split()[1] == pos:
		posSet.add(tmp)
	else:
		negSet.add(tmp)

#size of version space
count = 2**((2**4) - len(posSet) - len(negSet))
print count
trainfile.close()
#test on 4Cat-Dev.labeled
testfile = open(sys.argv[1], 'r')

for line in testfile:
	words = line.split('\t')
	tmp = 0
	tmp += (words[0].split()[1] == 'Male') << 0;
	tmp += (words[1].split()[1] == 'Young') << 1;
	tmp += (words[2].split()[1] == 'Yes') << 2;
	tmp += (words[3].split()[1] == 'Yes') << 3;
	if tmp in posSet:
		numpos, numneg = count, 0
	elif tmp in negSet:
		numpos, numneg = 0, count
	else:
		numpos, numneg = count/2, count/2
	print numpos, numneg
testfile.close()