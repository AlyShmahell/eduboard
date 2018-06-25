import hashlib
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys

class audio_randomness(object):
	
	@classmethod	
	def get_randaudio(cls, batch_size, list_len):
		cls.batch_size = batch_size
		cls.list_len = list_len
		cls.record_sample()
		cls.hash_sample()
		return cls.return_as_np_array()
		
	@classmethod	
	def record_sample(cls):
		try:
			if cls.batch_size%128 != 0:
				raise ValueError('batch_size needs to be multiples of 128')
			if cls.list_len < 7:
				raise ValueError('list_len needs to be larger than 7')
		except ValueError as e:
			sys.exit(e)
		frequency = int(cls.batch_size/128)*1000*int(cls.list_len/7)
		frequency += (1000*int(cls.batch_size/128),0)[cls.list_len%7==0]
		duration = 0.001
		cls.recoding_sample = sd.rec(int(duration * frequency), samplerate=frequency, channels=2,dtype='float64')
		sd.wait()
		
	@classmethod	
	def hash_sample(cls):
		cls.hashed_sample = [hashlib.sha512(z).hexdigest() for y,z in enumerate(cls.recoding_sample)]
	
	@classmethod	
	def return_as_np_array(cls):
		intermediate_array = [cls.normalize("{:b}".format(x)) for y, z in enumerate(cls.hashed_sample) for x in bytearray(z, 'ascii')]
		intermediate_array = [intermediate_array[i] if i<cls.batch_size*int(cls.list_len/7) else intermediate_array[i][0:(cls.list_len%7)] for i,_ in enumerate(intermediate_array)]
		np.random.shuffle(intermediate_array)
		intermediate_array = [j for i in intermediate_array for j in i]
		return np.array(intermediate_array).reshape(cls.batch_size, cls.list_len)
	
	@classmethod	
	def normalize(cls, a):
		return [int(b)*2-1 for b in (a,'0'+a)[len(a)<7]]
	
	
	
class grey_repr(object):
	
	@classmethod
	def get_grey_repr(cls,np_array):
		x, y = np.array(np_array).shape
		print('orig', x, y)
		grey_rep = np.reshape(np_array,cls.redimentionalize(x, y))
		print('gre', grey_rep.shape)
		plt.subplot(111)
		imgplot = plt.imshow(grey_rep, cmap='gray')
		plt.show()
	
	@classmethod
	def redimentionalize(cls, a, b):
		width = max(a,b)
		height = min(a,b)
		while width%2 == 0 and width/2 >= height*2:
			width /= 2
			height *= 2
		return (int(width), int(height))
