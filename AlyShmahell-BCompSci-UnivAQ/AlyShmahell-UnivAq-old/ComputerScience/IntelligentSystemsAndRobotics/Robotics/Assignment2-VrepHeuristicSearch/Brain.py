# Copyright 2016 Aly Shmahell

# libraries
from VrepAPIWrapper import *


# initiation
initFunction()


# the brain of the robot: the "Think" part
def thinkFunction():
	moveState=True
	currPointDifference=[0,0,0]
	while True:
		detectionState, detectedPoint, detectedObjectHandle, wallState = senseFunction()
		# Debugging
		if detectionState:
			backwardModeUntilTime=time.time()+1
			while time.time()<backwardModeUntilTime:
				currPointDifference[0]=currPointDifference[0]-detectedPoint[0]
				currPointDifference[1]=currPointDifference[1]-detectedPoint[1]
				if currPointDifference[0]<currPointDifference[1]:
					actuateFunction(1,0)
				elif currPointDifference[0]>=currPointDifference[1]:
					actuateFunction(0,1)
			currPointDifference=[0,0,0]
			moveState=True
		else:
			if wallState:
				print('There is a Wall on the side!\n')
				actuateFunction(2,4)
			else:
				if moveState:
					print('I think I found an Exit\n')
					actuateFunction(2,4)
					moveState=False
				actuateFunction(4, 4)
			
# the main function
if __name__ == "__main__":
	try:
		thinkFunction()
	except KeyboardInterrupt:
		finishFunction()
		


