import sys
scoreMatrix = []
database = []
sequences = []

def score(nucSeq, nucDB):
	if nucSeq == nucDB:
		print "M"
	else:
		print "N"

def ngpa():
	for i in sequences:
		for j in database:
			print "first shift"
			for k in range(len(i)):
				for l,m in zip(range(k,len(i)),range(len(j))):
					score(i[l],j[m])
			print "second shift"
			for k in range(len(j)):
				for l,m in zip(range(k,len(j)),range(len(i))):
					score(j[l],i[m])


if __name__=='__main__':
	scoreMatrixFile = open("./ngpaScore").read()
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
	temporary = []
	for i in databaseFile:
		if i=='\n':
			database.append(temporary)
			temporary = []
		else:
			temporary.append(i)
	print(database)

	sequencesFile = open("./ngpaSequences").read()
	temporary = []
	for i in sequencesFile:
		if i=='\n':
			sequences.append(temporary)
			temporary = []
		else:
			temporary.append(i)

	print(sequences)

	ngpa()
