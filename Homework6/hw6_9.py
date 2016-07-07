#!/usr/bin/python
file = open('dc-bike-sharing.csv')
count = 0
total = 0.0
totalcnt = 0
totaltemp = 0.0
temp2 = 0.0
for line in file:
	count += 1
	if count > 1:
		words = line.split(',')
		temp = float(words[9])
		cnt = int(words[-1])
		total += temp * cnt
		totaltemp += temp
		totalcnt += cnt
		temp2 += temp ** 2



count -= 1
file.close()

cov = (total/float(count)) - (totaltemp/float(count)) * (totalcnt/float(count))
var = temp2/float(count) - ((totaltemp/float(count)) ** 2)
beta = cov/var
alpha = (totalcnt/float(count)) - beta * (totaltemp/float(count))
beta = round(beta,2)
alpha = round(alpha,2)
print alpha
print beta

file = open('dc-bike-sharing.csv')
count = 0
err = 0.0
for line in file:
	count += 1
	if count > 1:
		words = line.split(',')
		temp = float(words[9])
		cnt = int(words[-1])
		err += (cnt - (alpha + beta * temp))**2



count -= 1
file.close()
print round(err/float(count),2)
print round(alpha + beta * 0.55,2)
