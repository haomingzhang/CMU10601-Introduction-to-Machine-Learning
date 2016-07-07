#!/usr/bin/python
from numpy import *
file = open('dc-bike-sharing.csv')
count = 0
totalcnt = 0
totaltemp = 0.0
temp2 = 0.0
x = []
y = []
for line in file:
	count += 1
	if count > 1:
		words = line.split(',')
		temp = float(words[9])
		hum = float(words[11])
		cnt = float(words[-1])
		x.append([temp, hum, 1])
		y.append(cnt)

count -= 1
X = matrix(x)
Y = matrix(y)
beta = (((X.T)*X).I)*((X.T)*(Y.T))

c1 = round(beta[2,0],2)
c2 = round(beta[0,0],2)
c3 = round(beta[1,0],2)

#beta = matrix(c2,c3,c1)
print c1
print c2
print c3

#print Y.shape
#print beta.shape
#print X.shape

err = Y - beta.T * X.T
print round((err * err.T)[0,0] / count,2)
print round(c1+c2*0.55+c3*0.46,2)
file.close()

