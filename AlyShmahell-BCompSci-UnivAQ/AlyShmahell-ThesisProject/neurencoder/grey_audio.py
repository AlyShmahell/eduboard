import hashlib
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class audio_randomness(object):
	
	@classmethod	
	def get_randaudio(cls, batch_size):
		cls.record_sample(batch_size)
		cls.hash_sample()
		return cls.return_as_np_array()
		
	@classmethod	
	def record_sample(cls, batch_size):
		try:
			if batch_size%128 != 0:
				raise ValueError(
				    'batch_size needs to be multiples of 128'
				)
		except ValueError as e:
			sys.exit(e)
			
		frequency = (batch_size/128)*1000
		duration = 0.001
		cls.recoding_sample = sd.rec(int(duration * frequency), samplerate=frequency, channels=2,dtype='float64')
		sd.wait()
		
	@classmethod	
	def hash_sample(cls):
		cls.hashed_sample = [hashlib.sha512(z).hexdigest() for y,z in enumerate(cls.recoding_sample)]
	
	@classmethod	
	def return_as_np_array(cls):
		return [cls.normalize("{:b}".format(x)) for y, z in enumerate(cls.hashed_sample) for x in bytearray(z, 'ascii')]
	
	@classmethod	
	def normalize(cls, a):
		return [int(b)*2-1 for b in (a,'0'+a)[len(a)<7]]
	
	
	
class grey_repr(object):
	
	@classmethod
	def get_grey_repr(cls,np_array):
		x,  y = cls.get_array_dims(np_array)
		grey_rep = np.reshape(np_array,cls.redimentionalize(x , y))
		plt.subplot(111)
		imgplot = plt.imshow(grey_rep, cmap='gray')
		plt.show()
	
	@classmethod	
	def get_array_dims(cls, np_array):
		fst_dim = 7
		scnd_dim = len(np_array)
		return fst_dim, scnd_dim
	
	@classmethod
	def redimentionalize(cls, a, b):
		width = max(a,b)
		height = min(a,b)
		while width%2 == 0 and width/2>=height*2:
			width = width/2
			height = height*2
		return (int(width), int(height))

if __name__ == '__main__':
	rand_audio = audio_randomness.get_randaudio(512)
	grey_repr.get_grey_repr(rand_audio)

