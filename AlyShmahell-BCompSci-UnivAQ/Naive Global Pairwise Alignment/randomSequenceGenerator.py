# I used this simple generator to produce my database and sequence files
# argv[1] represents how many files you want
# argv[2] represents the length ratio of each sequence in the file
# argv[3] is the root name of the files you want
import sys
import random
alphabet = ['A','T','G','C']
for i in range(1,int(sys.argv[1])):
	sequences = ""
	for j in range(1,i*10):
		sequence = ""
		for l in range(1,j*int(sys.argv[2])):
			sequence+=random.choice(alphabet)
		sequences += sequence
		sequences += "\n"
	with open(sys.argv[3]+str(i),'wr') as database:
		database.write(sequences)
