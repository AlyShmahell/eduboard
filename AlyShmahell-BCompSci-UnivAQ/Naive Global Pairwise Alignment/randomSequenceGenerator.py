import sys
import random
alphabet = ['A','T','G','C']
for i in range(1,10):
	sequences = ""
	for j in range(i*10):
		for k in range(1,10):
			sequence = ""
			for l in range(k*100):
				sequence+=random.choice(alphabet)
			sequences += sequence
			sequences += "\n"
	with open("ngpaDatabase"+str(i),'wr') as database:
		database.write(sequences)
