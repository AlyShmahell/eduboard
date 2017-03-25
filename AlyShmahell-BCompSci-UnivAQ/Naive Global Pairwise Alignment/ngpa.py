import sys

scoreMatrixFile = open("./ngpaScore").read()
scoreMatrix = []
temporary = []
for i in scoreMatrixFile:
	if i==' ':
		continue
	else:
		if i=='\n':
			scoreMatrix.append(temporary)
			temporary = []
		else:
			temporary.append(int(i))

for i in scoreMatrix:
	print(i)

databaseFile = open("./ngpaDatabase").read()
database = []
temporary = []
for i in databaseFile:
	if i=='\n':
		database.append(temporary)
		temporary = []
	else:
		temporary.append(i)
print(database)

sequencesFile = open("./ngpaSequences").read()
sequences = []
temporary = []
for i in sequencesFile:
	if i=='\n':
		sequences.append(temporary)
		temporary = []
	else:
		temporary.append(i)

print(sequences)

for i in sequences:
	for j in database:
		print "first shift"
		for k in range(len(i)):
			for l,m in zip(range(k,len(i)),range(len(j))):
					if i[l]==j[m]:
						print "M"
					else:
						print "N"
		print "second shift"
		for k in range(len(j)):
			for l,m in zip(range(k,len(j)),range(len(i))):
					if j[l]==i[m]:
						print "M"
					else:
						print "N"
				
