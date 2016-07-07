#!/usr/bin/python

# haomingz
import sys
fstop = open (sys.argv[2],'r')
stopwords = set([])
for line in fstop:
	stopwords.add(line.strip())
f = open(sys.argv[1],'r')
words = {}
for line in f:
	wordsList = line.strip().lower().split()
	for w in wordsList:
		if w not in stopwords:
			if words.has_key(w):
				words[w] += 1
			else:
				words[w] = 1
result = sorted(words.items(), reverse=True)
r = ''
for w in result:
	r += w[0] + ':' + str(w[1]) + ','
sys.stdout.write(r[:-1])