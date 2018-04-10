import tensorflow as tf
from argparse import ArgumentParser
from neurencoder_asymmetric import *

def argparser_function():
	argparser = ArgumentParser()
	argparser.add_argument('-symmetric', action='store_true')
	argparser.add_argument('-asymmetric', action='store_true')
	return argparser
    
if __name__ == '__main__':
	cmd_argmuments = argparser_function().parse_args()
	# config=tf.ConfigProto(log_device_placement=True)
	with tf.Session() as tfsession:
		neurencoder = NeurEncoder(tfsession)
