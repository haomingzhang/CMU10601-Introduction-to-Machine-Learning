import sys
from math import *

#computes log sum of two exponentiated log numbers efficiently
def log_sum(left,right):
	if right < left:
		return left + log1p(exp(right - left))
	elif left < right:
		return right + log1p(exp(left - right));
	else:
		return left + log1p(1)


def forward(word, last):
	curr = []
	#initialize
	if last == None:
		for i in range(len(states)):
			state = states[i]
			curr.append(prior[state]+emit[state][word])
	#iteration
	else:
		for i in range(len(states)):
			state_i = states[i]
			for j in range(len(states)):
				state_j = states[j]
				if trans[state_j].has_key(state_i):
					tran_j_i = trans[state_j][state_i]
					if j==0:
						mysum = last[j]+tran_j_i
					else:
						mysum = log_sum(mysum, last[j]+tran_j_i)
			mysum += emit[state_i][word]
			curr.append(mysum)
		
	return curr


trans = {}
states = []
emit = {}
prior = {}
#trans
transfile = open(sys.argv[2])
for line in transfile:
	line = line.strip()
	words = line.split(' ')
	states.append(words[0])
	d = {}
	for i in range(1,len(words)):
		tmp = words[i].split(':')
		d[tmp[0]] = log(float(tmp[1]))
	trans[words[0]] = d
transfile.close()

#emit
emitfile = open(sys.argv[3])
for line in emitfile:
	line = line.strip()
	words = line.split(' ')
	d = {}
	for i in range(1,len(words)):
		tmp = words[i].split(':')
		d[tmp[0]] = log(float(tmp[1]))
	emit[words[0]] = d
emitfile.close()


priorfile = open(sys.argv[4])
for line in priorfile:
	line = line.strip()
	words = line.split(' ')
	prior[words[0]] = log(float(words[1]))
priorfile.close();



devfile = open(sys.argv[1])
for line in devfile:
	words = line.strip().split(' ')
	last = None
	for word in words:
		last = forward(word, last)
	mysum = last[0]
	for i in range(1,len(last)):
		mysum = log_sum(mysum,last[i])
	print mysum

devfile.close()