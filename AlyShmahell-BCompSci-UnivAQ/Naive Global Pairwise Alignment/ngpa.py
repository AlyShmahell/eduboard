import sys
import math

scoree = open("./score").read()
print(scoree)

array = []
subarray = []
for i in scoree:
	if i==' ':
		continue
	else:
		if i=='\n':
			array.append(subarray)
			subarray = []
		else:
			subarray.append(int(i))
print(array)

