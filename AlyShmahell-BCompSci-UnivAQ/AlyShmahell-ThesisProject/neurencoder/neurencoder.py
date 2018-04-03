import tensorflow as tf
import numpy as np
import matplotlib
import matplotlib.pyplot as pyplot
import seaborn
from hyper_parameters import *

class NeurEncoder(object):
	def __init__(self, sess):

		self.sess = sess
		self.msg_len = MSG_LEN
		self.key_len = KEY_LEN
		self.batch_size = BATCH_SIZE
		self.epochs = EPOCHS
		self.iterations = ITERATIONS
		self.learning_rate = LEARNING_RATE
		self.FILTERS = [
				[RAW_FILTERS[0][0], 1, RAW_FILTERS[0][2]],
				[RAW_FILTERS[1][0], RAW_FILTERS[0][2], RAW_FILTERS[1][2]],
				[RAW_FILTERS[2][0], RAW_FILTERS[1][2], RAW_FILTERS[2][2]],
				[RAW_FILTERS[3][0], RAW_FILTERS[2][2], 1]
				]
		self.model_NoFCL = {'alice': Model_NoFCL[0], 'bob': Model_NoFCL[1], 'eve': 2*(Model_NoFCL[0]+Model_NoFCL[1])}
		self.build_model()
		self.train()
		
	def build_1D_convolution(self, layer, filter_shape, stride, name):
		with tf.variable_scope(name):
			weight_filter = tf.get_variable('w', shape=filter_shape, initializer=tf.contrib.layers.xavier_initializer())
			return tf.nn.conv1d(layer, weight_filter, stride, padding='SAME')
		
	def build_4_1D_convolutions(self, hidden_layer, name):
		convolution_0 = tf.nn.leaky_relu(self.build_1D_convolution(hidden_layer, self.FILTERS[0], stride=1, name=name+'_conv0'))
		convolution_1 = tf.nn.leaky_relu(self.build_1D_convolution(convolution_0, self.FILTERS[1], stride=2, name=name+'_conv1'))
		convolution_2 = tf.nn.leaky_relu(self.build_1D_convolution(convolution_1, self.FILTERS[2], stride=1, name=name+'_conv2'))
		convolution_3 = tf.nn.tanh(self.build_1D_convolution(convolution_2, self.FILTERS[3], stride=1, name=name+'_conv3'))
		return convolution_3
	
	def gen_data(self, tensor_rank_multiplier):
		return (np.random.randint(0, 2, size=(tensor_rank_multiplier, self.msg_len))*2-1),\
		   	(np.random.randint(0, 2, size=(tensor_rank_multiplier, self.key_len))*2-1)

	def build_net(self, name, net_input, no_of_FC_layers):
		fc_layer = tf.nn.sigmoid(tf.matmul(net_input, self.weights[name][0]))
		for i in range(no_of_FC_layers-1):
			fc_layer = tf.nn.sigmoid(tf.matmul(fc_layer, self.weights[name][i+1]))
		hidden_layer = tf.expand_dims(fc_layer, 2)
		net = tf.squeeze(self.build_4_1D_convolutions(hidden_layer, name))
		return net

	def build_model(self):
		self.placeholders = {
					'msg': tf.placeholder("float", [None, self.msg_len]),
					'key': tf.placeholder("float", [None, self.key_len])
					}
		self.weights = {}
		for net_name in self.model_NoFCL:
			self.weights[net_name] = [tf.get_variable(
							net_name+"_w"+str(NoFCL), 
							[(self.key_len,0)[net_name=='eve' and NoFCL==0]+self.msg_len,
							 self.key_len+self.msg_len],
								initializer=tf.contrib.layers.xavier_initializer()) 
										for NoFCL in range(self.model_NoFCL[net_name])]

		self.alice = self.build_net('alice', 
					tf.concat([self.placeholders['msg'], self.placeholders['key']],1), self.model_NoFCL['alice'])
		self.bob = self.build_net('bob', tf.concat([self.alice, self.placeholders['key']],1), self.model_NoFCL['bob'])
		self.eve = self.build_net('eve', self.alice, self.model_NoFCL['eve'])
		
		self.loss_functions = {
					'bob': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.bob)),
						tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.bob))
						 + (1. - tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.eve))) ** 2.],
					'eve': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.eve))]
					}
		
		training_variables_raw = tf.trainable_variables()
		self.training_variables = {
					'bob' : [var for var in training_variables_raw if 'alice_' in var.name or 'bob_' in var.name],
					'eve': [var for var in training_variables_raw if 'eve_' in var.name]
					}
		
		self.optimizers = {
					'bob': [tf.train.AdamOptimizer(self.learning_rate).minimize(
						self.loss_functions['bob'][1], var_list=self.training_variables['bob'])],
					'eve': [tf.train.AdamOptimizer(self.learning_rate).minimize(
						self.loss_functions['eve'][0], var_list=self.training_variables['eve'])]
					}
		
		self.errors = {
				'bob': [],
				'eve': []
				}
	def train(self):
		tf.global_variables_initializer().run()
		for epoch in range(1, self.epochs+1):
			print ('Training Alice and Bob, Epoch:', epoch)
			msg_val, key_val = self.gen_data(tensor_rank_multiplier=self.batch_size)
			self.iterate('bob', msg_val, key_val)
			print ('Training Eve, Epoch:', epoch)
			msg_val, key_val = self.gen_data(tensor_rank_multiplier=self.batch_size*2)
			self.iterate('eve', msg_val, key_val)
		self.display_results()

	def iterate(self, network, msg_val, key_val):
		for i in range(self.iterations):
			exercise = self.sess.run(
						[self.optimizers[network], self.loss_functions[network][0]],
						feed_dict={self.placeholders['msg']: msg_val, self.placeholders['key']: key_val})
			self.errors[network].append(exercise[1])

	def display_results(self):
		seaborn.set_style("whitegrid")
		pyplot.plot([epoch for epoch in range(1, (self.epochs*self.iterations)+1)], self.errors['bob'])
		pyplot.plot([epoch for epoch in range(1, (self.epochs*self.iterations)+1)], self.errors['eve'])
		pyplot.legend(['bob', 'eve'])
		pyplot.xlabel(str(self.epochs*self.iterations)+' iterations in '+str(self.epochs)+' epochs')
		pyplot.ylabel('decryption errors')
		pyplot.show()

if __name__ == '__main__':
	with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
		neurencoder = NeurEncoder(sess)
