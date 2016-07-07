import sys
from math import *




def viterbi_func(word, last, q):
	curr = []
	new_q = []
	#initialize
	if last == None:
		for i in range(len(states)):
			state = states[i]
			curr.append(prior[state]+emit[state][word])
			new_q.append([i])
	#iteration
	else:
		for i in range(len(states)):
			state_i = states[i]
			for j in range(len(states)):
				state_j = states[j]
				if trans[state_j].has_key(state_i):
					tran_j_i = trans[state_j][state_i]
					if j==0:
						mymax = last[j]+tran_j_i+emit[state_i][word]
						max_index = 0
					else:
						tmp=last[j]+tran_j_i+emit[state_i][word]
						if tmp > mymax:
							mymax = tmp
							max_index = j
			curr.append(mymax)
			new_q.append(q[max_index][:])
			new_q[i].append(i)

	return [curr, new_q]


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
	q = None
	for word in words:
		last, q = viterbi_func(word, last, q)
	result = q[last.index(max(last))]
	for i in range(len(words)):
		print words[i]+'_'+states[result[i]],
	print

devfile.close()