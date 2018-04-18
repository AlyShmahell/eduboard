import tensorflow as tf
import numpy as np
import matplotlib
import matplotlib.pyplot as pyplot
import seaborn
import json
import sys
import datetime

class general_hyper_parameters(object):
	def __init__(self):
		self.hyper_parameters = json.load(open('hyper_parameters.json'))
		'''
		' checking if the filter matrix shape and values are correct
		'''
		try:
			if np.shape(self.hyper_parameters['filters'])!=(4,3):
				raise ValueError('there is something wrong with filters\' shape inside hyper_parameters.json')
			if np.array_equal(self.hyper_parameters['filters'],
						[
							[self.hyper_parameters['filters'][0][0], 1, self.hyper_parameters['filters'][0][2]],
							[self.hyper_parameters['filters'][1][0], self.hyper_parameters['filters'][0][2], self.hyper_parameters['filters'][1][2]],
							[self.hyper_parameters['filters'][2][0], self.hyper_parameters['filters'][1][2], self.hyper_parameters['filters'][2][2]],
							[self.hyper_parameters['filters'][3][0], self.hyper_parameters['filters'][2][2], 1]
						]) == False:
				raise ValueError('there is something wrong with filter values inside hyper_parameters.json')
		except ValueError as e:
			sys.exit(e)
			
class asymmetric_hyper_parameters(general_hyper_parameters, object):
	def __init__(self):
		super(asymmetric_hyper_parameters ,self).__init__()
		self.hyper_parameters['No_of_FC_Layers']['eve'] = 2*(self.hyper_parameters['No_of_FC_Layers']['alice']+
							 		self.hyper_parameters['No_of_FC_Layers']['bob']+
							 		self.hyper_parameters['No_of_FC_Layers']['pub_key_gen']+
							 		self.hyper_parameters['No_of_FC_Layers']['priv_key_gen'])
							 		
class symmetric_hyper_parameters(general_hyper_parameters, object):
	def __init__(self):
		super(symmetric_hyper_parameters ,self).__init__()
		self.hyper_parameters['No_of_FC_Layers']['eve'] = 2*(self.hyper_parameters['No_of_FC_Layers']['alice']+
							 		self.hyper_parameters['No_of_FC_Layers']['bob'])

class model_builder(general_hyper_parameters, object):
	def __init(self):
		super(model_builder, self).__init__();
	def build_1D_convolution(self, layer, filter_shape, stride, name):
		with tf.variable_scope(name):
			weight_filter = tf.get_variable('w', shape=filter_shape, initializer=tf.contrib.layers.xavier_initializer())
			return tf.nn.conv1d(layer, weight_filter, stride, padding='SAME')
		
	def build_4_1D_convolutions(self, hidden_layer, name):
		convolution_0 = tf.nn.leaky_relu(
			self.build_1D_convolution(hidden_layer, self.hyper_parameters["filters"][0], stride=1, name=name+'_conv0'))
		convolution_1 = tf.nn.leaky_relu(
			self.build_1D_convolution(convolution_0, self.hyper_parameters["filters"][1], stride=2, name=name+'_conv1'))
		convolution_2 = tf.nn.leaky_relu(
			self.build_1D_convolution(convolution_1, self.hyper_parameters["filters"][2], stride=1, name=name+'_conv2'))
		convolution_3 = tf.nn.tanh(
			self.build_1D_convolution(convolution_2, self.hyper_parameters["filters"][3], stride=1, name=name+'_conv3'))
		return convolution_3
	
	def gen_data(self, tensor_rank_multiplier):
		return (np.random.randint(0, 2, size=(tensor_rank_multiplier, self.hyper_parameters["msg_len"]))*2-1),\
		   	(np.random.randint(0, 2, size=(tensor_rank_multiplier, self.hyper_parameters["key_seed_len"]))*2-1)

	def build_net(self, net_name, net_input, no_of_FC_layers, halved_first_layer_flag=False):
		weights = [tf.get_variable(net_name+"_w"+str(NoFCL), 
						[(self.hyper_parameters["key_seed_len"],0)[halved_first_layer_flag==True and NoFCL==0]+self.hyper_parameters["msg_len"], 
							self.hyper_parameters["key_seed_len"]+self.hyper_parameters["msg_len"]],
								initializer=tf.contrib.layers.xavier_initializer()) 
										for NoFCL in range(self.hyper_parameters["No_of_FC_Layers"][net_name])]
		fc_layer = tf.nn.sigmoid(tf.matmul(net_input, weights[0]))
		for i in range(1, no_of_FC_layers):
			fc_layer = tf.nn.sigmoid(tf.matmul(fc_layer, weights[i]))
		hidden_layer = tf.expand_dims(fc_layer, 2)
		net = tf.squeeze(self.build_4_1D_convolutions(hidden_layer, net_name))
		return net

class model_data(general_hyper_parameters, object):
	def __init__(self):
		super(model_data, self).__init__()
		self.placeholders = {
					'msg': tf.placeholder("float", [None, self.hyper_parameters["msg_len"]]),
					'key_seed': tf.placeholder("float", [None, self.hyper_parameters["key_seed_len"]])
					}
		self.errors = {
				'bob': [],
				'eve': []
				}	

class asymmetric_model(asymmetric_hyper_parameters, model_builder, model_data, object):
	def __init__(self):
		super(asymmetric_model, self).__init__()
	def build_model(self):
		self.pub_key_generator = self.build_net('pub_key_gen', self.placeholders['key_seed'],
						self.hyper_parameters["No_of_FC_Layers"]['pub_key_gen'], True)
		self.priv_key_generator = self.build_net('priv_key_gen', self.pub_key_generator,
						self.hyper_parameters["No_of_FC_Layers"]['priv_key_gen'], True)
		self.alice = self.build_net('alice', 
					tf.concat([self.placeholders['msg'], self.pub_key_generator],1),
							self.hyper_parameters["No_of_FC_Layers"]['alice'])
		self.bob = self.build_net('bob', tf.concat([self.alice, self.priv_key_generator],1),
							self.hyper_parameters["No_of_FC_Layers"]['bob'])
		
		self.eve = self.build_net('eve', tf.concat([self.alice,self.pub_key_generator], 1), 
							self.hyper_parameters["No_of_FC_Layers"]['eve'])
		
		self.loss_functions = {
					'bob': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.bob)),
						tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.bob))
						 + (1. - tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.eve))) ** 2.],
					'eve': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.eve))]
					}
		
		self.training_variables_raw = tf.trainable_variables()
		self.training_variables = {
					'bob' : [var for var in self.training_variables_raw if 'alice_' in var.name or 'bob_' in var.name],
					'eve': [var for var in self.training_variables_raw if 'eve_' in var.name]
					}
		
		self.optimizers = {
					'bob': [tf.train.AdamOptimizer(
						self.hyper_parameters["learning_rate"]).minimize(
							self.loss_functions['bob'][1], 
								var_list=self.training_variables['bob'])],
					'eve': [tf.train.AdamOptimizer(self.hyper_parameters["learning_rate"]).minimize(
							self.loss_functions['eve'][0], var_list=self.training_variables['eve'])]
					}	
				
class symmetric_model(symmetric_hyper_parameters, model_builder, model_data, object):
	def __init__(self):
		super(symmetric_model, self).__init__()
	def build_model(self):
		self.alice = self.build_net('alice', 
					tf.concat([self.placeholders['msg'], self.placeholders['key_seed']],1), self.hyper_parameters["No_of_FC_Layers"]['alice'])
		self.bob = self.build_net('bob', tf.concat([self.alice, self.placeholders['key_seed']],1), self.hyper_parameters["No_of_FC_Layers"]['bob'])
		self.eve = self.build_net('eve', self.alice, self.hyper_parameters["No_of_FC_Layers"]['eve'], True)
		
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
					'bob': [tf.train.AdamOptimizer(self.hyper_parameters["learning_rate"]).minimize(
						self.loss_functions['bob'][1], var_list=self.training_variables['bob'])],
					'eve': [tf.train.AdamOptimizer(self.hyper_parameters["learning_rate"]).minimize(
						self.loss_functions['eve'][0], var_list=self.training_variables['eve'])]
					}
		

class model_trainer(model_builder, object):
	def __init__(self):
		super(model_trainer, self).__init__()
	def train(self):
		tf.global_variables_initializer().run()
		model_saver = tf.train.Saver()
		for epoch in range(1, self.hyper_parameters["epochs"]+1):
			asthetics_param_friends = ('',' and their friends')[self.scheme=='asymmetric']
			print ('Training Alice, Bob'+asthetics_param_friends+' - Epoch:', epoch)
			msg_val, key_seed_val = self.gen_data(tensor_rank_multiplier=self.hyper_parameters["batch_size"])
			self.iterate('bob', msg_val, key_seed_val)
			print ('Training Eve, Epoch:', epoch)
			msg_val, key_seed_val = self.gen_data(tensor_rank_multiplier=self.hyper_parameters["batch_size"]*2)
			self.iterate('eve', msg_val, key_seed_val)
		model_saver.save(self.tfsession, './saved_model_data/neurencoder-'+self.scheme+'-model-'+datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"));
	def iterate(self, network, msg_val, key_seed_val):
		for i in range(self.hyper_parameters["iterations"]):
			exercise = self.tfsession.run(
						[self.optimizers[network], self.loss_functions[network][0]],
						feed_dict={self.placeholders['msg']: msg_val, self.placeholders['key_seed']: key_seed_val})
			self.errors[network].append(exercise[1])

	def display_results(self):
		seaborn.set_style("whitegrid")
		pyplot.plot([epoch for epoch in range(1, (self.hyper_parameters["epochs"]*self.hyper_parameters["iterations"])+1)], self.errors['bob'])
		pyplot.plot([epoch for epoch in range(1, (self.hyper_parameters["epochs"]*self.hyper_parameters["iterations"])+1)], self.errors['eve'])
		pyplot.legend(['bob', 'eve'])
		pyplot.xlabel(str(self.hyper_parameters["epochs"]*self.hyper_parameters["iterations"])+' iterations in '
				+str(self.hyper_parameters["epochs"])+' epochs')
		pyplot.ylabel('decryption errors')
		pyplot.savefig('./saved_model_data/neurencoder-'+self.scheme+'-plot_figure-'+datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")+'.svg')
		pyplot.show()
		
class symmetric_neurencoder(symmetric_model, model_trainer, object):
	def __init__(self, tfsession, scheme):
		self.tfsession = tfsession
		self.scheme = scheme
		super(symmetric_neurencoder, self).__init__()
		self.build_model()
		self.train()
		self.display_results()
		
class asymmetric_neurencoder(asymmetric_model, model_trainer, object):
	def __init__(self, tfsession, scheme):
		self.tfsession = tfsession
		self.scheme = scheme
		super(asymmetric_neurencoder, self).__init__()
		self.build_model()
		self.train()
		self.display_results()
		
class neurencoder(object):
	def __init__(self, tfsession, scheme):
		self.tfsession = tfsession
		self.scheme = scheme
		self.return_cryptosys()	
	def return_cryptosys(self):
		if self.scheme == 'symmetric':
			self.cryptosys = symmetric_neurencoder(self.tfsession, self.scheme)
		else:
			self.cryptosys = asymmetric_neurencoder(self.tfsession, self.scheme)
		return self.cryptosys
