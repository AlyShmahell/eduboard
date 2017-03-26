import sys
import random
alphabet = ['A','T','G','C']
for i in range(1,6):
	sequences = ""
	for j in range(i*10):
		for k in range(1,10):
			sequence = ""
			for l in range(k*10):
				sequence+=random.choice(alphabet)
			sequences += sequence
			sequences += "\n"
	with open("DNAinput"+str(i),'wr') as database:
		database.write(sequences)
