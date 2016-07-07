#!/usr/bin/python

# haomingz
import sys
f = open(sys.argv[1],'r')
words = set([])
for line in f:
	wordsList = line.strip().lower().split()
	for w in wordsList:
		words.add(w)
result = sorted(list(words), reverse=True)
r = ''
for w in result:
	r += w + ','
sys.stdout.write(r[:-1])