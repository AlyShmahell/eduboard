# Copyright 2016 Aly Shmahell

# libraries
from VrepAPIWrapper import *


# initiation
initFunction()


# the brain of the robot: the "Think" part
def thinkFunction():
	backwardModeUntilTime=time.time()
	currPointDifference=[0,0,0]
	while True:
		detectionState, detectedPoint, detectedObjectHandle = senseFunction()
		print(detectionState)
		if (detectionState):
			backwardModeUntilTime=time.time()+1

		if time.time()<backwardModeUntilTime:
			currPointDifference[0]=currPointDifference[0]-detectedPoint[0]
			currPointDifference[2]=currPointDifference[2]-detectedPoint[2]
			print (detectedPoint)
			if currPointDifference[0]<currPointDifference[2]:
				actuateFunction(1,0)
			elif currPointDifference[0]>=currPointDifference[2]:
				actuateFunction(0,1)
		else:
			actuateFunction(8.0, 8.0)

# the main function
if __name__ == "__main__":
	try:
		thinkFunction()
	except KeyboardInterrupt:
		finishFunction()
		


