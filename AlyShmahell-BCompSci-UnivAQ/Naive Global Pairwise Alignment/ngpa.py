import sys
import numpy as np
scoreMatrix = []
database = []
sequences = []
metadata = []

def score(nucSeq, nucDB):
	return scoreMatrix[metadata.index(nucSeq)][metadata.index(nucDB)]

def ngpa():
	for i in sequences:
		totalmax = -1000000000
		for j in database:
			print "first shift"
			submax = -1000000000
			totalmax = max(totalmax,submax)
			for k in range(len(i)):
				alignmentscore = 0
				for l,m in zip(range(k,len(i)),range(len(j))):
					alignmentscore = alignmentscore + score(i[l],j[m])
				submax = max(submax,alignmentscore)
			print "second shift"
			totalmax = max(totalmax,submax)
			for k in range(len(j)):
				alignmentscore = 0
				for l,m in zip(range(k,len(j)),range(len(i))):
					alignmentscore = alignmentscore + score(j[l],i[m])
				submax = max(submax,alignmentscore)
			totalmax = max(totalmax,submax)
		print totalmax


if __name__=='__main__':
	with open('ngpaMetadata') as metadataFile:
		metadata =[item for sublist in map(list,(value.rstrip('\n') for value in metadataFile)) for item in sublist] 
	print metadata
	with open('ngpaScore') as scoreMatrixFile:
		scoreMatrix = [[int(value) for value in line.split()] for line in scoreMatrixFile]
	print scoreMatrix

	with open(sys.argv[1],'r') as databaseFile:
		temporary = []
		for i in databaseFile.read():
			if i=='\n':
				database.append(temporary)
				temporary = []
			else:
				temporary.append(i)
		print(database)

	with open(sys.argv[2],'r') as sequencesFile:
		temporary = []
		for i in sequencesFile.read():
			if i=='\n':
				sequences.append(temporary)
				temporary = []
			else:
				temporary.append(i)

		print(sequences)

	ngpa()
