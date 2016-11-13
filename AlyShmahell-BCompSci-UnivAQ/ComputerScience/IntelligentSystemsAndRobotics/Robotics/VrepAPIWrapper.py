# Copyright 2016 Aly Shmahell

# libraries
import sys
sys.path.insert(0, './VrepPythonAPI')
import vrep

# define clientID as a global variable
clientID = 0

# initiation function
def initFunction():
	# close previously opened connections
	vrep.simxFinish(-1)

	# connect to Vrep
	clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) 
	if clientID!=-1:
		print ('Connected to remote API server')
	else:
		sys.exit('Connection Failed!')

# main loop
def mainLoop(leftSpeed, rightSpeed):
	while True:
		# connect to motors
		errorCode,leftHandle=vrep.simxGetObjectHandle(clientID,'dr12_leftJoint_',vrep.simx_opmode_oneshot_wait)
		errorCode,rightHandle=vrep.simxGetObjectHandle(clientID,'dr12_rightJoint_',vrep.simx_opmode_oneshot_wait)
		# initiate movement with a normal speed
		errorCode=vrep.simxSetJointTargetVelocity(clientID, leftHandle, leftSpeed, vrep.simx_opmode_oneshot_wait)
		errorCode=vrep.simxSetJointTargetVelocity(clientID, rightHandle, rightSpeed, vrep.simx_opmode_oneshot_wait)
		# connect to sensor
		errorCode,sensorHandle=vrep.simxGetObjectHandle(clientID,'dr12_bumperForceSensor_',vrep.simx_opmode_streaming)
		return sensorHandle

# when the program ends, inform of a successful operation
print('there are no problems!')
