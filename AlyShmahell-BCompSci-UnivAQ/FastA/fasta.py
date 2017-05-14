# Crude FastA Implementation
# Author: Aly Shmahell
# Copyrights: Aly Shmahell 2017
# Usage: python fasta.py <database filename> <sequences filename>
# Example: python fasta.py ./databaseFiles/database ./sequenceFiles/sequences

import sys
import time
import datetime
import operator

scoreMatrix = []
database = []
sequences = []
alphabet = []

# counts the occurances of every unique element in a list, orders them by value, and returns their count
def count(superlist):
	dictionary = {}
	for normalist in superlist:
		for sublist in normalist:
			if sublist[0] in dictionary:
				dictionary[sublist[0]] += 1
			else:
				dictionary[sublist[0]] = 1
	
	return sorted(dictionary.items(), key=operator.itemgetter(1))

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

def fasta():
	# starting session log
	log()
	for inputSequence in sequences:
		startTime = time.time()
		maxScore = -1000000000
		highScoreSequence = []
		# populating seqWordTable
		seqWordTable = [[] for i in range(len(alphabet))]
		for nucSeqPos,nucSeq in enumerate(inputSequence):
			seqWordTable[alphabet.index(nucSeq)].append(nucSeqPos)
		# testing each database sequence against the input sequence at hand
		for databaseSequence in database:
			subScore = -1000000000
			maxScore = max(maxScore,subScore)
			# populating dbWordTable
			dbWordTable = [[] for i in range(len(alphabet))]
			for nucDbPos,nucDb in enumerate(databaseSequence):
				dbWordTable[alphabet.index(nucDb)].append(nucDbPos)
			# populating offset table
			offsetTable = [[] for i in range(len(alphabet))]
			for nucCount in range(4):
				for seqWordTableVal in seqWordTable[nucCount]:
					for dbWordTableVal in dbWordTable[nucCount]:
						offsetTable[nucCount].append([seqWordTableVal-dbWordTableVal,[seqWordTableVal,dbWordTableVal]])
			# scoring
			print offsetTable
			print ("\n")
			print count(offsetTable)
			print ("\n")
				
				
			
	
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
	fasta()
