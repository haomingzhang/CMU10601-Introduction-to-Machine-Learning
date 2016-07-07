#!/usr/bin/python
from numpy import *
import sys
import random
import time
t0 = time.time()
result=[]
eta = 1
iter_num = 20000
#number of hidden units
num_hidden = 2
num_attrs = 5 + 1
# w[to_id][from_id]
# w0 ... wn
w = []
w_out = []
h_out = []
#init_value = 0.2
for i in range(0, num_hidden):
	init_w=[]
	for j in range(0, num_attrs):
		init_w.append(random.uniform(-0.5,0.5))
	w.append(array(init_w))

for h in range(0, num_hidden):
	w_out.append(random.uniform(-0.5,0.5))
	h_out.append(0.0)

w_out = array(w_out)
h_out = array(h_out)

trainfile = open(sys.argv[1])
trainset = []
traint = []
count = 0
for line in trainfile:
	count += 1
	if count > 1:
		nums = [0.5]
		words = line.strip().split(',')
		traint.append(float(words[-1])/100.0)
		for k in range(0,num_attrs-1):
			nums.append(float(words[k])/100.0)
		trainset.append(array(nums))

count -= 1
trainfile.close()


for iteration in range(0,iter_num):
	if time.time()-t0 > 160:
		break
	#train
	k = 0
	for trainline in trainset:
		t = traint[k]
		#print t,
		x = trainline
		#print x
		for h in range(0,num_hidden):
			h_out[h] = 1/(1+(e**(-dot(x,w[h]))))


		out = 1/(1+(e**(-dot(h_out, w_out))))
		#print out
		delta_out = out*(1-out)*(t-out)
		delta_h = h_out*(1-h_out)*w_out*delta_out
		#update weight_h
		w_out += eta*delta_out*h_out

		#update weight_x_to_h
		for h in range(0,num_hidden):
			w[h] += (eta*delta_h[h])*x
		k += 1

	#compute error
	total_error = 0.0
	k = 0
	for trainline in trainset:
		t = traint[k] * 100
		x = trainline
		for h in range(0,num_hidden):
			h_out[h] = 1/(1+(e**(-dot(x,w[h]))))

		out = 100/(1+(e**(-dot(h_out, w_out))))
		#print t, out
		total_error += (t-out)**2
		k += 1

	result.append(total_error)

for r in result:
	print r
print 'TRAINING COMPLETED! NOW PREDICTING.'
testfile = open(sys.argv[2])
count = 0
for line in testfile:
	count += 1
	if count > 1:
		nums = [0.5]
		words = line.strip().split(',')
		for word in words:
			nums.append(float(word)/100.0)
		x = array(nums)
		for h in range(0,num_hidden):
			h_out[h] = (1/(1+(e**(-dot(x,w[h])))))

		out = 100/(1+(e**(-dot(h_out, w_out))))
		print out
testfile.close()