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
totalvocab = len(s)

condefault = math.log(1.0/(conn+totalvocab))
libdefault = math.log(1.0/(libn+totalvocab))

wordscon = []
wordslib = []
for key in s:
	dictcon[key] = float(dictcon[key]+1)/(conn+totalvocab)
	wordscon.append([dictcon[key], key])
	dictlib[key] = float(dictlib[key]+1)/(libn+totalvocab)
	wordslib.append([dictlib[key], key])
wordscon.sort(reverse=True)
wordslib.sort(reverse=True)

for i in range(0,20):
	print wordslib[i][1] + " %.04f" % wordslib[i][0]

print ""

for i in range(0,20):
	print wordscon[i][1] + " %.04f" % wordscon[i][0]





	