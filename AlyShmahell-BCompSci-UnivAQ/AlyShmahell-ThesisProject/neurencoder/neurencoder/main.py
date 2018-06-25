from core_classes import *

if __name__ == '__main__':

	# config=tf.ConfigProto(log_device_placement=True)
	with tf.Session() as tfsession:
		neurencoder = neurencoder(tfsession)
