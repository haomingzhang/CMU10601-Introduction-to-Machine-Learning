#!/usr/bin/python
import math
import sys

train = open(sys.argv[1])

dictlib = {}
dictcon = {}
conn = 0
libn = 0
condoc = 0
libdoc = 0
s = set()
for line in train:

	# 0 for con, 1 for lib
	if line.startswith("con"):
		flag = 0
		condoc += 1
	else:
		flag = 1
		libdoc += 1

	traintext = open(line.strip())

	for ori_word in traintext:
		word = ori_word.strip().lower()
		s.add(word)
		if flag == 0:
			conn += 1
			if dictcon.has_key(word):
				dictcon[word] += 1
			else:
				dictcon[word] = 1
			if not dictlib.has_key(word):
				dictlib[word] = 0
		else:
			libn += 1
			if dictlib.has_key(word):
				dictlib[word] += 1
			else:
				dictlib[word] = 1
			if not dictcon.has_key(word):
				dictcon[word] = 0
	traintext.close()

train.close()
prior_con = math.log(condoc/float(condoc+libdoc))
prior_lib = math.log(libdoc/float(condoc+libdoc))
#print math.e**prior_con, math.e**prior_lib


wordsfreq = []
for key in s:
	wordsfreq.append([dictlib[key]+dictcon[key], key])
wordsfreq.sort(reverse=True)
N = int(sys.argv[3])
for i in range(0, N):
	s.remove(wordsfreq[i][1])
	conn -= dictcon[wordsfreq[i][1]]
	libn -= dictlib[wordsfreq[i][1]]
totalvocab = len(s)
for key in s:
	dictcon[key] = math.log(float(dictcon[key]+1)/(conn+totalvocab))
	dictlib[key] = math.log(float(dictlib[key]+1)/(libn+totalvocab))



test = open(sys.argv[2])
totaltest = 0
correct = 0
for line in test:
	totaltest += 1
	if line.startswith("con"):
		flag = 0
	else:
		flag = 1

	testtext = open(line.strip())
	pcon = prior_con
	plib = prior_lib
	for ori_word in testtext:
		word = ori_word.strip().lower()
		if word in s:
			if dictcon.has_key(word):
				pcon += dictcon[word]
			if dictlib.has_key(word):
				plib += dictlib[word]

	testtext.close()

	if pcon > plib:
		print "C"
		if flag == 0:
			correct += 1
	else:
		print "L"
		if flag == 1:
			correct += 1

test.close()
accuracy = float(correct)/totaltest
print "Accuracy: %.04f" % accuracy
