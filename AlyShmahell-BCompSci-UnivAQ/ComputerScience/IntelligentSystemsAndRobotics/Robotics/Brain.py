import sys
sys.path.insert(0, './VrepPythonAPI')
import vrep

vrep.simxFinish(-1) # just in case, close all opened connections

clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP

if clientID!=-1:
	print ('Connected to remote API server')
else:
	sys.exit('Connection Failed!')

errorCode,leftHandle=vrep.simxGetObjectHandle(clientID,'dr12_leftJoint_',vrep.simx_opmode_oneshot_wait)
errorCode,rightHandle=vrep.simxGetObjectHandle(clientID,'dr12_rightJoint_',vrep.simx_opmode_oneshot_wait)

errorCode=vrep.simxSetJointTargetVelocity(clientID, leftHandle, 1.0,vrep.simx_opmode_oneshot_wait)
errorCode=vrep.simxSetJointTargetVelocity(clientID, rightHandle, 1.0,vrep.simx_opmode_oneshot_wait)

errorCode,rightHandle=vrep.simxGetObjectHandle(clientID,'dr12_bumperForceSensor_',vrep.simx_opmode_streaming)


print('there are no problems!')
