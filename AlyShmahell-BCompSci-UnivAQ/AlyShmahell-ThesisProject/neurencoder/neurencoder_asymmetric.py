import tensorflow as tf
import numpy as np
import matplotlib
import matplotlib.pyplot as pyplot
import seaborn
from hyper_parameters_asymmetric import *

class NeurEncoder(object):
	def __init__(self, tfsession):

		self.tfsession = tfsession
		self.msg_len = MSG_LEN
		self.key_seed_len = kEY_SEED_LEN
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
		self.model_NoFCL = {'alice': Model_NoFCL[0], 'bob_pub_gen': Model_NoFCL[1], 'bob_priv_gen': Model_NoFCL[1], 'bob_decrypter': Model_NoFCL[1], 'eve': 2*(Model_NoFCL[0]+Model_NoFCL[1]+Model_NoFCL[2]+Model_NoFCL[3])}
		self.build_model()
		self.train()
		self.display_results()
		
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
		   	(np.random.randint(0, 2, size=(tensor_rank_multiplier, self.key_seed_len))*2-1)

	def build_net(self, net_name, net_input, no_of_FC_layers):
		weights = [tf.get_variable(net_name+"_w"+str(NoFCL), 
						[(self.key_seed_len,0)['_gen' in net_name and NoFCL==0]+self.msg_len, 
							self.key_seed_len+self.msg_len],
								initializer=tf.contrib.layers.xavier_initializer()) 
										for NoFCL in range(self.model_NoFCL[net_name])]
		fc_layer = tf.nn.sigmoid(tf.matmul(net_input, weights[0]))
		for i in range(1, no_of_FC_layers):
			fc_layer = tf.nn.sigmoid(tf.matmul(fc_layer, weights[i]))
		hidden_layer = tf.expand_dims(fc_layer, 2)
		net = tf.squeeze(self.build_4_1D_convolutions(hidden_layer, net_name))
		return net

	def build_model(self):
		self.placeholders = {
					'msg': tf.placeholder("float", [None, self.msg_len]),
					'key_seed': tf.placeholder("float", [None, self.key_seed_len])
					}

		self.bob_pub_key_generator = self.build_net('bob_pub_gen', self.placeholders['key_seed'],
						self.model_NoFCL['bob_pub_gen'])
		self.bob_priv_key_generator = self.build_net('bob_priv_gen', self.bob_pub_key_generator,
						self.model_NoFCL['bob_priv_gen'])
		self.alice = self.build_net('alice', 
					tf.concat([self.placeholders['msg'], self.bob_pub_key_generator],1), self.model_NoFCL['alice'])
		self.bob_decrypter = self.build_net('bob_decrypter', tf.concat([self.alice, self.bob_priv_key_generator],1),
					self.model_NoFCL['bob_decrypter'])
		
		self.eve = self.build_net('eve', tf.concat([self.alice,self.bob_pub_key_generator], 1), self.model_NoFCL['eve'])
		
		self.loss_functions = {
					'bob_decrypter': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.bob_decrypter)),
						tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.bob_decrypter))
						 + (1. - tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.eve))) ** 2.],
					'eve': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.eve))]
					}
		
		self.training_variables_raw = tf.trainable_variables()
		self.training_variables = {
					'bob_decrypter' : [var for var in self.training_variables_raw if 'alice_' in var.name or 'bob_' in var.name],
					'eve': [var for var in self.training_variables_raw if 'eve_' in var.name]
					}
		
		self.optimizers = {
					'bob_decrypter': [tf.train.AdamOptimizer(self.learning_rate).minimize(
						self.loss_functions['bob_decrypter'][1], var_list=self.training_variables['bob_decrypter'])],
					'eve': [tf.train.AdamOptimizer(self.learning_rate).minimize(
						self.loss_functions['eve'][0], var_list=self.training_variables['eve'])]
					}
		
		self.errors = {
				'bob_decrypter': [],
				'eve': []
				}
	def train(self):
		tf.global_variables_initializer().run()
		model_saver = tf.train.Saver()
		for epoch in range(1, self.epochs+1):
			print ('Training Alice and Bob, Epoch:', epoch)
			msg_val, key_seed_val = self.gen_data(tensor_rank_multiplier=self.batch_size)
			self.iterate('bob_decrypter', msg_val, key_seed_val)
			print ('Training Eve, Epoch:', epoch)
			msg_val, key_seed_val = self.gen_data(tensor_rank_multiplier=self.batch_size*2)
			self.iterate('eve', msg_val, key_seed_val)
		model_saver.save(self.tfsession, './neurencoder-asymmetric-model');

	def iterate(self, network, msg_val, key_seed_val):
		for i in range(self.iterations):
			exercise = self.tfsession.run(
						[self.optimizers[network], self.loss_functions[network][0]],
						feed_dict={self.placeholders['msg']: msg_val, self.placeholders['key_seed']: key_seed_val})
			self.errors[network].append(exercise[1])

	def display_results(self):
		seaborn.set_style("whitegrid")
		pyplot.plot([epoch for epoch in range(1, (self.epochs*self.iterations)+1)], self.errors['bob_decrypter'])
		pyplot.plot([epoch for epoch in range(1, (self.epochs*self.iterations)+1)], self.errors['eve'])
		pyplot.legend(['bob_decrypter', 'eve'])
		pyplot.xlabel(str(self.epochs*self.iterations)+' iterations in '+str(self.epochs)+' epochs')
		pyplot.ylabel('decryption errors')
		pyplot.show()
