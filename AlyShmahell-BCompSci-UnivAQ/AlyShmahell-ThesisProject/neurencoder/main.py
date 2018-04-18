import argparse
import sys
class scheme_option(object):
	def __init__(self):
		scheme = self.parse_arguments().symmetric + self.parse_arguments().asymmetric
		if len(scheme) > 0 and len(scheme) < 11:
			self.scheme = scheme
			return
		sys.exit('choose one shceme, and one scheme only')
	def parse_arguments(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('-symmetric', action='store_const', dest='symmetric',
				    const='symmetric',
				    default = '',
				    help='choses the symmetric model')
		parser.add_argument('-asymmetric', action='store_const', dest='asymmetric',
				    const='asymmetric',
				    default = '',
				    help='choses the asymmetric model')
		return parser.parse_args()

from neurencoder import *
if __name__ == '__main__':
	# config=tf.ConfigProto(log_device_placement=True)
	start_time = datetime.datetime.now()
	with tf.Session() as tfsession:
		neurencoder = neurencoder(tfsession, scheme_option().scheme)
	end_time = datetime.datetime.now()
	uptime = end_time - start_time
	print('Uptime: '+str(uptime))
	with open('./saved_model_data/neurencoder-'+scheme_option().scheme+'-Uptime-'+datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), "w") as uptime_outfile:
		uptime_outfile.write(str(uptime))
