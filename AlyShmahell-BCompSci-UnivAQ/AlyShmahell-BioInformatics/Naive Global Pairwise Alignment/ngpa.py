# Naive Global Pairwise Alignment
# Author: Aly Shmahell
# Copyrights: Aly Shmahell 2017
# Usage: python ngpa.py <database filename> <sequences filename>
# Example: python ngpa.py ./databaseFiles/database9 ./sequenceFiles/sequences5

import sys
import time
import datetime

scoreMatrix = []
database = []
sequences = []
alphabet = []

# retrieves `correspondent pairwise substitution score` from the score matrix
def findScore(nucSeq, nucDB):
	return scoreMatrix[alphabet.index(nucSeq)][alphabet.index(nucDB)]

# display and log
def output(array,score,computeTime):
	string = ""
	for value in array:
		string+=str(value)
	string += (" ... sequence scored: " + str(score) + " ... time to compute: " + str(computeTime) + " seconds \n")
	print string
	with open('log.txt','a') as log:
		log.write(string)

# logging session upstart
def log():
	with open('log.txt','a') as log:
		log.write("Session started at: " + str(datetime.datetime.now()) + "\n")
	

def ngpa():
	# starting session log
	log()
	# going over each input sequence
	for inputSequence in sequences:
		startTime = time.time()
		maxScore = -1000000000
		highScoreSequence = []
		# testing each database sequence against the input sequence at hand
		for databaseSequence in database:
			subScore = -1000000000
			maxScore = max(maxScore,subScore)
			# forward pass on inputSequence
			for counter in range(len(inputSequence)):
				alignmentscore = 0
				for dynamicShift,staticShift in zip(range(counter,len(inputSequence)),range(len(databaseSequence))):
					alignmentscore = alignmentscore + findScore(inputSequence[dynamicShift],databaseSequence[staticShift])
				subScore = max(subScore,alignmentscore)
			# storing the results of the forward pass
			if subScore > maxScore:
				highScoreSequence = databaseSequence
			maxScore = max(maxScore,subScore)
			# backward pass on databaseSequence
			for counter in range(len(databaseSequence)):
				alignmentscore = 0
				for dynamicShift,staticShift in zip(range(counter,len(databaseSequence)),range(len(inputSequence))):
					alignmentscore = alignmentscore + findScore(databaseSequence[dynamicShift],inputSequence[staticShift])
				subScore = max(subScore,alignmentscore)
			# storing the results of the backward pass
			if subScore > maxScore:
				highScoreSequence = databaseSequence
			maxScore = max(maxScore,subScore)
		# outputting results
		output(highScoreSequence,maxScore,time.time()-startTime)



if __name__=='__main__':
	# using list mapping to reduce a file to a 1 dimentional array of alphabet
	with open('metadata') as metadataFile:
		alphabet =[item for sublist in map(list,(value.rstrip('\n') for value in metadataFile)) for item in sublist]
	# using line splitting and integer conversion to input the score matrix
	with open('scoreMatrix') as scoreMatrixFile:
		scoreMatrix = [[int(value) for value in line.split()] for line in scoreMatrixFile]
	# inputting the database as a terminal parameter with paying attention to new lines
	with open(sys.argv[1],'r') as databaseFile:
		database = [[value for value in line.rstrip('\n')] for line in databaseFile]
	# inputting the sequencesFile as a terminal parameter with paying attention to new lines
	with open(sys.argv[2],'r') as sequencesFile:
		sequences = [[value for value in line.rstrip('\n')] for line in sequencesFile]
	ngpa()
