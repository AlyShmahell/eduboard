# Copyright 2016 Aly Shmahell

# libraries
import sys
import time
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
		actuateFunction(4.0, 4.0)
	else:
		sys.exit('Connection Failed!')

# actuation function: sends speed information to the motors
def actuateFunction(leftSpeed, rightSpeed):
	# connect to motors
	errorCode,leftHandle=vrep.simxGetObjectHandle(clientID,'dr12_leftJoint_',vrep.simx_opmode_oneshot_wait)
	errorCode,rightHandle=vrep.simxGetObjectHandle(clientID,'dr12_rightJoint_',vrep.simx_opmode_oneshot_wait)
	# initiate movement with a normal speed
	errorCode=vrep.simxSetJointTargetVelocity(clientID, leftHandle, leftSpeed, vrep.simx_opmode_oneshot_wait)
	errorCode=vrep.simxSetJointTargetVelocity(clientID, rightHandle, rightSpeed, vrep.simx_opmode_oneshot_wait)

# sensory function: returns collision information from the bumper
def senseFunction():
	# connect to sensor
	errorCode,sensorHandle=vrep.simxGetObjectHandle(clientID,'dr12_bumperForceSensor_',vrep.simx_opmode_streaming)
	returncode, state, force,torque=vrep.simxReadForceSensor(clientID, sensorHandle, vrep.simx_opmode_streaming)
	return state, force

# when the program ends, inform of a successful operation
if clientID==-1:
	print('there are no problems!')
