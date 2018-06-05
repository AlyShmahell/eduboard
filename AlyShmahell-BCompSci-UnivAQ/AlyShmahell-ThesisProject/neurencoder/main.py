import argparse
import sys
from neurencoder import *

'''
class scheme_option(object):
	def __init__(self):
		scheme = self.parse_arguments().symmetric + self.parse_arguments().asymmetric + self.parse_arguments().hybrid
		if len(scheme) > 0 and len(scheme) < 17:
			self.scheme = scheme
			return
		sys.exit('choose one shceme, and one scheme only')
		
	def parse_arguments(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('-symmetric', action='store_const', dest='symmetric',
				    const='symmetric',
				    default = '',
				    help='chooses the symmetric model')
		parser.add_argument('-asymmetric', action='store_const', dest='asymmetric',
				    const='asymmetric',
				    default = '',
				    help='chooses the asymmetric model')
		parser.add_argument('-hybrid', action='store_const', dest='hybrid',
				    const='hybrid',
				    default = '',
				    help='chooses the hybrid model')
		return parser.parse_args()
'''

if __name__ == '__main__':

	# config=tf.ConfigProto(log_device_placement=True)
	with tf.Session() as tfsession:
		neurencoder = neurencoder(tfsession)
