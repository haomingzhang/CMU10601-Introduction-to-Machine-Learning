#!/usr/bin/python
file = open('dc-bike-sharing.csv')
count = 0
count2 = 0
count3 = 0
q11 = 0
q12 = 0
totaltemp = 0.0
totalatemp = 0.0
totalhum = 0.0
q6 = 0.0
q7 = 0.0
temp2 = 0.0
hum2 = 0.0
cnt1 = 0
cnt2 = 0
cnt3 = 0
for line in file:
	count += 1
	if count > 1:
		words = line.split(',')
		dteday = words[1]
		yr = int(words[3])
		mnth = int(words[4])
		weather = int(words[8])
		temp = float(words[9])
		atemp = float(words[10])
		hum = float(words[11])
		cnt = int(words[-1])

		totaltemp += temp
		totalhum += hum
		totalatemp += atemp
		temp2 += temp ** 2
		hum2 += hum ** 2
		q6 += temp * atemp
		q7 += temp * hum

		if mnth>3 and mnth<11:
			q11 += 1
			if hum>0.6 and weather==2:
				q12 += 1

		if temp<0.3:
			cnt1 += cnt
			count2 += 1

		if temp>0.3:
			cnt2 += cnt
			cnt3 += cnt ** 2
			count3 += 1




count -= 1
file.close()
#print count
print round(float(q12)/float(q11),2)
print round(totaltemp/float(count),2)
print round(totalhum/float(count),2)
print round(cnt1/float(count2),2)
print round(cnt3/float(count3) - ((cnt2/float(count3)) ** 2),2)
print round((q6/float(count)) - (totaltemp/float(count)) * (totalatemp/float(count)),2)
cov = (q7/float(count)) - (totaltemp/float(count)) * (totalhum/float(count))
dtemp = (temp2/float(count) - ((totaltemp/float(count)) ** 2))**0.5
dhum = (hum2/float(count) - ((totalhum/float(count)) ** 2))**0.5
print round(cov/dtemp/dhum,2)