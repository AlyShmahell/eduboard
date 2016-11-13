# Copyright 2016 Aly Shmahell

# libraries
from VrepAPIWrapper import *


# initiation
initFunction()

# the brain of the robot: sense-calculate-act
def brain():
	backwardModeUntilTime=time.time()
	while True:
		state, force = senseFunction()
		if state>0:
			if abs(force[1])>1 or abs(force[2])>1:
				backwardModeUntilTime=time.time()+2
			if time.time()<backwardModeUntilTime:
				actuateFunction(-2.0, 0)
			else:
				actuateFunction(8.0, 8.0)

# the main function
if __name__ == "__main__":
	try:
		brain()
	except KeyboardInterrupt:
		actuateFunction(0, 0)
		


