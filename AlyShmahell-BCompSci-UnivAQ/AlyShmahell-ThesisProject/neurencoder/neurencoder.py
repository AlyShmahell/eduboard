import tensorflow as tf
import numpy as np
import matplotlib
import matplotlib.pyplot as pyplot
import seaborn
import json
import sys
import datetime
import progressbar

class general_hyper_parameters(object):

	def __init__(self):
		print('general_hyper_parameters', 'initiated')
		self.hyper_parameters = json.load(open('hyper_parameters.json'))
		'''
		' checking if the filter matrix shape and values are correct
		'''
		try:
			if np.shape(self.hyper_parameters['filters'])!=(4,3):
				raise ValueError('there is something wrong with filters\' shape inside hyper_parameters.json')
			if np.array_equal(self.hyper_parameters['filters'],
						[
							[self.hyper_parameters['filters'][0][0], 
							1, 
							self.hyper_parameters['filters'][0][2]],
							[self.hyper_parameters['filters'][1][0], 
							self.hyper_parameters['filters'][0][2], 
							self.hyper_parameters['filters'][1][2]],
							[self.hyper_parameters['filters'][2][0], 
							self.hyper_parameters['filters'][1][2], 
							self.hyper_parameters['filters'][2][2]],
							[self.hyper_parameters['filters'][3][0], 
							self.hyper_parameters['filters'][2][2], 
							1]
						]) == False:
				raise ValueError('there is something wrong with filter values inside hyper_parameters.json')
		except ValueError as e:
			sys.exit(e)
			
			
class asymmetric_hyper_parameters(object):

	def __init__(self):
		print('asymmetric_hyper_parameters', 'initiated')
		self.hyper_parameters['No_of_FC_Layers']['eve'] = 2*(self.hyper_parameters['No_of_FC_Layers']['alice']+
							 		self.hyper_parameters['No_of_FC_Layers']['bob']+
							 		self.hyper_parameters['No_of_FC_Layers']['pub_key_gen']+
							 		self.hyper_parameters['No_of_FC_Layers']['priv_key_gen'])
		self.hyper_parameters['No_of_FC_Layers']['alan'] = self.hyper_parameters['No_of_FC_Layers']['eve']
					
							 		
class symmetric_hyper_parameters(object):

	def __init__(self):
		print('symmetric_hyper_parameters', 'initiated')
		self.hyper_parameters['No_of_FC_Layers']['eve'] = 2*(self.hyper_parameters['No_of_FC_Layers']['alice']+
							 		self.hyper_parameters['No_of_FC_Layers']['bob'])
		self.hyper_parameters['No_of_FC_Layers']['alan'] = self.hyper_parameters['No_of_FC_Layers']['eve']


class model_builder(object):

	def __init__(self):
		print('model_builder', 'initiated')
		
	random_binary = lambda self, shape, dtype, partition_info=None:\
				(tf.random_uniform(shape, minval = 0, maxval = 2, dtype=dtype)*2-1)

	def build_1D_convolution(self, layer, build_mode, filter_shape, stride, name):
		if build_mode == 'TRAINING':
			with tf.variable_scope(name):
				weight_filter = tf.get_variable('w', shape=filter_shape, 
					initializer=tf.contrib.layers.xavier_initializer())
				return tf.nn.conv1d(layer, weight_filter, stride, padding='SAME')
		else:
			weight_filter = self.graph.get_tensor_by_name(name+"/w:0")
			return tf.nn.conv1d(layer, weight_filter, stride, padding='SAME')
		
	def build_4_1D_convolutions(self, hidden_layer, name, build_mode):
		convolution_0 = tf.nn.leaky_relu(
			self.build_1D_convolution(hidden_layer, build_mode, 
				self.hyper_parameters["filters"][0], stride=1, name=name+'_conv0'))
		convolution_1 = tf.nn.leaky_relu(
			self.build_1D_convolution(convolution_0, build_mode, 
				self.hyper_parameters["filters"][1], stride=2, name=name+'_conv1'))
		convolution_2 = tf.nn.leaky_relu(
			self.build_1D_convolution(convolution_1, build_mode, 
				self.hyper_parameters["filters"][2], stride=1, name=name+'_conv2'))
		convolution_3 = tf.nn.tanh(
			self.build_1D_convolution(convolution_2, build_mode, 
				self.hyper_parameters["filters"][3], stride=1, name=name+'_conv3'))
		return convolution_3
	
	def gen_data(self, tensor_rank_multiplier):
		return (np.random.randint(0, 2, size=(tensor_rank_multiplier, self.hyper_parameters["msg_len"]))*2-1),\
		   	(np.random.randint(0, 2, size=(tensor_rank_multiplier, self.hyper_parameters["key_seed_len"]))*2-1)

	def build_net(self, net_name, net_input, no_of_FC_layers, build_mode, halved_first_layer_flag=False):
		if build_mode == 'TRAINING':
			self.weights = [tf.get_variable(net_name+"_w"+str(NoFCL), 
						[(self.hyper_parameters["key_seed_len"],0)
							[halved_first_layer_flag==True and NoFCL==0]
							+self.hyper_parameters["msg_len"], 
							self.hyper_parameters["key_seed_len"]+self.hyper_parameters["msg_len"]],
							initializer=tf.contrib.layers.xavier_initializer()) 
							for NoFCL in range(self.hyper_parameters["No_of_FC_Layers"][net_name])]
		else:
			self.graph = tf.get_default_graph()
			self.weights = [self.graph.get_tensor_by_name(net_name+"_w"+str(NoFCL)+":0")
					for NoFCL in range(self.hyper_parameters["No_of_FC_Layers"][net_name])]
		fc_layer = tf.nn.sigmoid(tf.matmul(net_input, self.weights[0]))
		for i in range(1, no_of_FC_layers):
			fc_layer = tf.nn.sigmoid(tf.matmul(fc_layer, self.weights[i]))
		hidden_layer = tf.expand_dims(fc_layer, 2)
		net = tf.squeeze(self.build_4_1D_convolutions(hidden_layer, net_name, build_mode))
		return net


class model_data(object):

	def __init__(self):
		print('model_data', 'initiated')
		self.placeholders = {
					'msg': tf.placeholder("float", [None, self.hyper_parameters["msg_len"]]),
					'key_seed': tf.placeholder("float", [None, self.hyper_parameters["key_seed_len"]]),
					'encrypted_msg': tf.placeholder("float", [None, self.hyper_parameters["msg_len"]]),
					'priv_key': tf.placeholder("float", [None, self.hyper_parameters["key_seed_len"]]),
					'pub_key': tf.placeholder("float", [None, self.hyper_parameters["key_seed_len"]])
					}
		self.errors = {
				'bob': [],
				'eve': [],
				'alan': []
				}
		
	def reset_errors(self):
		print('errors have been reset')
		self.errors = {
				'bob': [],
				'eve': [],
				'alan': []
				}


class asymmetric_training_model(object):

	def __init__(self):
		print('asymmetric_model', 'initiated')
		
	def build_training_model(self):
		self.networks = {}
		self.networks['pub_key_generator'] = self.build_net('pub_key_gen', self.placeholders['key_seed'],
						self.hyper_parameters["No_of_FC_Layers"]['pub_key_gen'], 'TRAINING', True)
		self.networks['priv_key_generator'] = self.build_net('priv_key_gen', self.networks['pub_key_generator'],
						self.hyper_parameters["No_of_FC_Layers"]['priv_key_gen'], 'TRAINING', True)
		self.networks['alice'] = self.build_net('alice', 
					tf.concat([self.placeholders['msg'], self.networks['pub_key_generator']],1),
							self.hyper_parameters["No_of_FC_Layers"]['alice'], 'TRAINING', False)
		self.networks['bob'] = self.build_net('bob', tf.concat([self.networks['alice'],
					self.networks['priv_key_generator']],1),
							self.hyper_parameters["No_of_FC_Layers"]['bob'], 'TRAINING', False)
		
		self.networks['eve'] = self.build_net('eve', tf.concat([self.networks['alice'], 
					self.networks['pub_key_generator']], 1), 
							self.hyper_parameters["No_of_FC_Layers"]['eve'], 'TRAINING', False)
		self.networks['alan'] = self.build_net('alan', tf.concat([self.networks['alice'], 
					self.networks['pub_key_generator']], 1), 
							self.hyper_parameters["No_of_FC_Layers"]['alan'], 'TRAINING', False)
		self.loss_functions = {
					'bob': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.networks['bob'])),
						tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.networks['bob']))
						 + (1. - tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.networks['eve'])))
						 ** 2.],
					'eve': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.networks['eve']))],
					'alan': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.networks['alan']))]
					}
		self.tf_trainable_variables = tf.trainable_variables()
		self.training_variables = {
					'bob' : [var for var in self.tf_trainable_variables if 'alice_' in var.name
						or 'bob_' in var.name or 'pub_key_gen' in var.name or 'priv_key_gen' in var.name],
					'eve': [var for var in self.tf_trainable_variables if 'eve_' in var.name],
					'alan': [var for var in self.tf_trainable_variables if 'alan_' in var.name]
					}
		self.optimizers = {
					'bob': [tf.train.AdamOptimizer(
						self.hyper_parameters["learning_rate"]).minimize(
							self.loss_functions['bob'][1], 
								var_list=self.training_variables['bob'])],
					'eve': [tf.train.AdamOptimizer(self.hyper_parameters["learning_rate"]).minimize(
							self.loss_functions['eve'][0], var_list=self.training_variables['eve'])],
					'alan': [tf.train.AdamOptimizer(self.hyper_parameters["learning_rate"]).minimize(
							self.loss_functions['alan'][0], var_list=self.training_variables['alan'])]
					}
					
					
class asymmetric_testing_model(object):
					
	def build_testing_model(self):
		print('build_testing_model', 'asymmetric', 'called')
		self.networks['pub_key_generator'] = self.build_net('pub_key_gen', self.placeholders['key_seed'],
						self.hyper_parameters["No_of_FC_Layers"]['pub_key_gen'], 'TESTING', True)
		self.networks['priv_key_generator'] = self.build_net('priv_key_gen', self.placeholders['pub_key'],
						self.hyper_parameters["No_of_FC_Layers"]['priv_key_gen'], 'TESTING', True)
		self.networks['alice'] = self.build_net('alice', 
					tf.concat([self.placeholders['msg'], self.placeholders['pub_key']],1),
							self.hyper_parameters["No_of_FC_Layers"]['alice'], 'TESTING', False)
		self.networks['bob'] = self.build_net('bob', tf.concat([self.placeholders['encrypted_msg'],
					self.placeholders['priv_key']],1),
							self.hyper_parameters["No_of_FC_Layers"]['bob'], 'TESTING', False)
		
		self.networks['eve'] = self.build_net('eve', tf.concat([self.placeholders['encrypted_msg'], 
					self.placeholders['pub_key']], 1), 
							self.hyper_parameters["No_of_FC_Layers"]['eve'], 'TESTING', False)
		self.networks['alan'] = self.build_net('alan', tf.concat([self.placeholders['encrypted_msg'], 
					self.placeholders['pub_key']], 1), 
							self.hyper_parameters["No_of_FC_Layers"]['alan'], 'TESTING', False)
				
				
class symmetric_training_model(object):

	def __init__(self):
		print('symmetric_model', 'initiated')
		
	def build_training_model(self):
		self.networks = {}
		self.networks['alice'] = self.build_net('alice', 
					tf.concat([self.placeholders['msg'], self.placeholders['key_seed']],1),
					self.hyper_parameters["No_of_FC_Layers"]['alice'], 'TRAINING', False)
		self.networks['bob'] = self.build_net('bob', tf.concat([self.networks['alice'], self.placeholders['key_seed']],1),
					self.hyper_parameters["No_of_FC_Layers"]['bob'], 'TRAINING', False)
		self.networks['eve'] = self.build_net('eve', self.networks['alice'], 
					self.hyper_parameters["No_of_FC_Layers"]['eve'], 'TRAINING', True)
		self.networks['alan'] = self.build_net('alan', self.networks['alice'], 
					self.hyper_parameters["No_of_FC_Layers"]['alan'], 'TRAINING', True)
		self.loss_functions = {
					'bob': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.networks['bob'])),
						tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.networks['bob']))
						 + (1. - tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.networks['eve'])))
						 ** 2.],
					'eve': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.networks['eve']))],
					'alan': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.networks['alan']))]
					}
		tf_trainable_variables = tf.trainable_variables()
		self.training_variables = {
					'bob' : [var for var in tf_trainable_variables if 'alice_' in var.name 
						or 'bob_' in var.name],
					'eve': [var for var in tf_trainable_variables if 'eve_' in var.name],
					'alan': [var for var in tf_trainable_variables if 'alan_' in var.name]
					}
		'''
		' debugging
		'
		for net in self.training_variables:
			for var in self.training_variables[net]:
				print(var)
		'''
			
		self.optimizers = {
					'bob': [tf.train.AdamOptimizer(self.hyper_parameters["learning_rate"]).minimize(
						self.loss_functions['bob'][1], var_list=self.training_variables['bob'])],
					'eve': [tf.train.AdamOptimizer(self.hyper_parameters["learning_rate"]).minimize(
						self.loss_functions['eve'][0], var_list=self.training_variables['eve'])],
					'alan': [tf.train.AdamOptimizer(self.hyper_parameters["learning_rate"]).minimize(
						self.loss_functions['alan'][0], var_list=self.training_variables['alan'])]
					}
					
					
class symmetric_testing_model(object):

	def build_testing_model(self):
		print('build_testing_model', 'symmetric', 'called')
		self.networks['alice'] = self.build_net('alice', 
					tf.concat([self.placeholders['msg'], self.placeholders['key_seed']],1),
					self.hyper_parameters["No_of_FC_Layers"]['alice'], 'TESTING', False)
		self.networks['bob'] = self.build_net('bob', tf.concat([self.placeholders['encrypted_msg'],
		 			self.placeholders['key_seed']],1),
		 			self.hyper_parameters["No_of_FC_Layers"]['bob'], 'TESTING', False)
		self.networks['eve'] = self.build_net('eve', self.placeholders['encrypted_msg'],
					self.hyper_parameters["No_of_FC_Layers"]['eve'], 'TESTING', True)
		self.networks['alan'] = self.build_net('alan', self.placeholders['encrypted_msg'],
					self.hyper_parameters["No_of_FC_Layers"]['alan'], 'TESTING', True)


class hybrid_training_model(object):

	def __init__(self):
		print('asymmetric_model', 'initiated')
		
	def build_training_model(self):
		self.networks = {}
		self.networks['pub_key_generator'] = self.build_net('pub_key_gen', self.placeholders['key_seed'],
						self.hyper_parameters["No_of_FC_Layers"]['pub_key_gen'], 'TRAINING', True)
		self.networks['priv_key_generator'] = self.build_net('priv_key_gen', self.networks['pub_key_generator'],
						self.hyper_parameters["No_of_FC_Layers"]['priv_key_gen'], 'TRAINING', True)
		self.networks['alice'] = self.build_net('alice', 
					tf.concat([self.placeholders['msg'], self.networks['pub_key_generator']],1),
							self.hyper_parameters["No_of_FC_Layers"]['alice'], 'TRAINING', False)
		self.networks['bob'] = self.build_net('bob', tf.concat([self.networks['alice'],
					self.networks['priv_key_generator']],1),
							self.hyper_parameters["No_of_FC_Layers"]['bob'], 'TRAINING', False)
		
		self.networks['eve'] = self.build_net('eve', self.networks['alice'], 
							self.hyper_parameters["No_of_FC_Layers"]['eve'], 'TRAINING', True)
		self.networks['alan'] = self.build_net('alan', self.networks['alice'], 
							self.hyper_parameters["No_of_FC_Layers"]['alan'], 'TRAINING', True)
		self.loss_functions = {
					'bob': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.networks['bob'])),
						tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.networks['bob']))
						 + (1. - tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.networks['eve'])))
						 ** 2.],
					'eve': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.networks['eve']))],
					'alan': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.networks['alan']))]
					}
		self.tf_trainable_variables = tf.trainable_variables()
		self.training_variables = {
					'bob' : [var for var in self.tf_trainable_variables if 'alice_' in var.name
						or 'bob_' in var.name or 'pub_key_gen' in var.name or 'priv_key_gen' in var.name],
					'eve': [var for var in self.tf_trainable_variables if 'eve_' in var.name],
					'alan': [var for var in self.tf_trainable_variables if 'alan_' in var.name]
					}
		self.optimizers = {
					'bob': [tf.train.AdamOptimizer(
						self.hyper_parameters["learning_rate"]).minimize(
							self.loss_functions['bob'][1], 
								var_list=self.training_variables['bob'])],
					'eve': [tf.train.AdamOptimizer(self.hyper_parameters["learning_rate"]).minimize(
							self.loss_functions['eve'][0], var_list=self.training_variables['eve'])],
					'alan': [tf.train.AdamOptimizer(self.hyper_parameters["learning_rate"]).minimize(
							self.loss_functions['alan'][0], var_list=self.training_variables['alan'])]
					}

					
class hybrid_testing_model(object):

	def build_testing_model(self):
		print('build_testing_model', 'hybrid', 'called')
		self.networks['alice'] = self.build_net('alice', 
					tf.concat([self.placeholders['msg'], self.placeholders['key_seed']],1),
					self.hyper_parameters["No_of_FC_Layers"]['alice'], 'TESTING', False)
		self.networks['bob'] = self.build_net('bob', tf.concat([self.placeholders['encrypted_msg'],
		 			self.placeholders['key_seed']],1),
		 			self.hyper_parameters["No_of_FC_Layers"]['bob'], 'TESTING', False)
		self.networks['eve'] = self.build_net('eve', self.placeholders['encrypted_msg'],
					self.hyper_parameters["No_of_FC_Layers"]['eve'], 'TESTING', True)
		self.networks['alan'] = self.build_net('alan', self.placeholders['encrypted_msg'],
					self.hyper_parameters["No_of_FC_Layers"]['alan'], 'TESTING', True)


class asymmetric_model_tester(object):

	def __init__(self):
		print('asymmetric_model_tester', 'initiated')
		
	def test(self):
		self.reset_errors()
		print('asymmetric_model_tester', 'running')
		self.model_saver = tf.train.Saver()
		for epoch in range(1, self.hyper_parameters["epochs"]+1):
			msg_val, key_seed_val = self.gen_data(tensor_rank_multiplier=self.hyper_parameters["batch_size"])
			print('Testing Key-Pair Generation - Epoch: ', epoch)
			self.iterate_pub_key_generation(key_seed_val)
			self.iterate_priv_key_generation()
			print('Testing Alice - Epoch: ', epoch)
			self.iterate_alice(msg_val)
			print('Testing Bob - Epoch: ', epoch)
			self.iterate_decryptors('bob', msg_val, key_seed_val)
			print('Testing eve - Epoch: ', epoch)
			self.iterate_decryptors('eve', msg_val, key_seed_val)
			print('Testing Alan - Epoch: ', epoch)
			self.iterate_decryptors('alan', msg_val, key_seed_val)
			
	def iterate_pub_key_generation(self, key_seed_val):
		iteration_progressbar = result_processor.progress_bar(steps=self.hyper_parameters["iterations"])
		for i in range(self.hyper_parameters["iterations"]):
			self.pub_key_val = self.tfsession.run(self.networks['pub_key_generator'],
						feed_dict={self.placeholders['key_seed']: key_seed_val})
			iteration_progressbar.update(i+1)
		iteration_progressbar.finish()
		
	def iterate_priv_key_generation(self):
		iteration_progressbar = result_processor.progress_bar(steps=self.hyper_parameters["iterations"])
		for i in range(self.hyper_parameters["iterations"]):
			self.priv_key_val = self.tfsession.run(self.networks['priv_key_generator'],
						feed_dict={self.placeholders['pub_key']: self.pub_key_val})
			iteration_progressbar.update(i+1)
		iteration_progressbar.finish()
		
	def iterate_alice(self, msg_val):
		iteration_progressbar = result_processor.progress_bar(steps=self.hyper_parameters["iterations"])
		for i in range(self.hyper_parameters["iterations"]):
			self.encrypted_msg_val = self.tfsession.run(self.networks['alice'],
						feed_dict={self.placeholders['msg']: msg_val,
						self.placeholders['pub_key']: self.pub_key_val})
			iteration_progressbar.update(i+1)
		iteration_progressbar.finish()
		
	def iterate_decryptors(self, network, msg_val, key_seed_val):
		iteration_progressbar = result_processor.progress_bar(steps=self.hyper_parameters["iterations"])
		for i in range(self.hyper_parameters["iterations"]):
			test_results = self.tfsession.run(
						self.loss_functions[network][0],
						feed_dict={self.placeholders['msg']: msg_val,
						self.placeholders['pub_key']: self.pub_key_val,
						self.placeholders['priv_key']: self.priv_key_val,
						self.placeholders['encrypted_msg']: self.encrypted_msg_val,
						self.placeholders['key_seed']: key_seed_val})
			self.errors[network].append(test_results)
			iteration_progressbar.update(i+1)
		iteration_progressbar.finish()

class symmetric_model_tester(object):

	def __init__(self):
		print('symmetric_model_tester', 'initiated')
		
	def test(self):
		self.reset_errors()
		print('symmetric_model_tester', 'running')
		self.model_saver = tf.train.Saver()
		for epoch in range(1, self.hyper_parameters["epochs"]+1):
			msg_val, key_seed_val = self.gen_data(tensor_rank_multiplier=self.hyper_parameters["batch_size"])
			print ('Testing Alice - Epoch:', epoch)
			self.iterate_alice(msg_val, key_seed_val)
			print ('Testing Bob - Epoch:', epoch)
			self.iterate_decryptors('bob', msg_val, key_seed_val)
			print ('Testing Eve - Epoch:', epoch)
			self.iterate_decryptors('eve', msg_val, key_seed_val)
			print ('Testing Alan - Epoch:', epoch)
			self.iterate_decryptors('alan', msg_val, key_seed_val)
			
	def iterate_alice(self, msg_val, key_seed_val):
		iteration_progressbar = result_processor.progress_bar(steps=self.hyper_parameters["iterations"])
		for i in range(self.hyper_parameters["iterations"]):
			self.encrypted_msg_val = self.tfsession.run(self.networks['alice'],
						feed_dict={self.placeholders['msg']: msg_val,
						self.placeholders['key_seed']: key_seed_val})
			iteration_progressbar.update(i+1)
		iteration_progressbar.finish()
		
	def iterate_decryptors(self, network, msg_val, key_seed_val):
		iteration_progressbar = result_processor.progress_bar(steps=self.hyper_parameters["iterations"])
		for i in range(self.hyper_parameters["iterations"]):
			test_results = self.tfsession.run(
						self.loss_functions[network][0],
						feed_dict={self.placeholders['msg']: msg_val,
						self.placeholders['key_seed']: key_seed_val,
						self.placeholders['encrypted_msg']: self.encrypted_msg_val})
			self.errors[network].append(test_results)
			iteration_progressbar.update(i+1)
		iteration_progressbar.finish()
			

class model_trainer(object):

	def __init__(self):
		print('model_trainer', 'initiated')
		
	def train(self):
		tf.global_variables_initializer().run()
		self.model_saver = tf.train.Saver()
		for epoch in range(1, self.hyper_parameters["epochs"]+1):
			msg_val, key_seed_val = self.gen_data(tensor_rank_multiplier=self.hyper_parameters["batch_size"])
			print ('Training Alice, Bob - Epoch:', epoch)
			self.iterate('bob', msg_val, key_seed_val)
			print ('Training Eve - Epoch:', epoch)
			self.iterate('eve', msg_val, key_seed_val)
			print ('Training Alan - Epoch:', epoch)
			msg_val, key_seed_val = self.gen_data(tensor_rank_multiplier=self.hyper_parameters["batch_size"])
			self.iterate('alan', msg_val, key_seed_val)
		
	def iterate(self, network, msg_val, key_seed_val):
		iteration_progressbar = result_processor.progress_bar(steps=self.hyper_parameters["iterations"])
		for i in range(self.hyper_parameters["iterations"]):
			exercise = self.tfsession.run(
						[self.optimizers[network], self.loss_functions[network][0]],
						feed_dict={self.placeholders['msg']: msg_val,
						self.placeholders['key_seed']: key_seed_val})
			self.errors[network].append(exercise[1])
			iteration_progressbar.update(i+1)
		iteration_progressbar.finish()


class result_processor:

	start_time = datetime.datetime.now()
	
	def process_uptime(scheme):
		uptime = datetime.datetime.now() - result_processor.start_time
		print('Uptime: '+str(uptime))
		with open('./saved_model_data/neurencoder-'
			+scheme
			+'-Uptime-'
			+datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), "w") as uptime_outfile:
			uptime_outfile.write(str(uptime))
			
	def process_results(scheme, errors, build_mode, x_scale, x_scale_caption, y_scale_caption):
		seaborn.set_style("whitegrid")
		legend = []
		for net_name in errors:
			pyplot.plot([epoch for epoch in range(1, (x_scale)+1)], errors[net_name])
			legend.append(net_name)
		pyplot.legend(legend)
		pyplot.xlabel(str(x_scale)+x_scale_caption)
		pyplot.ylabel(y_scale_caption)
		pyplot.savefig('./saved_model_data/neurencoder-'
				+scheme
				+"-"
				+build_mode
				+'-model-'
				+'-plot_figure-'
				+datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
				+'.svg')
		pyplot.show()
		
	def save_model(scheme, tfsession, model_saver, build_mode): 
		model_saver.save(tfsession,
				'./saved_model_data/neurencoder-'
				+scheme
				+"-"
				+build_mode
				+'-model-'+datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
	
	class progress_bar(object):
	
		def __init__(self, steps):
			self.current_progress_bar = progressbar.ProgressBar(maxval=steps,
										widgets=[progressbar.Bar('+', '[', ']'),
										' ', progressbar.Percentage()])
			self.current_progress_bar.start()
			
		def update(self, step):
			self.current_progress_bar.update(step)
			
		def finish(self):
			self.current_progress_bar.finish()
		
class neurencoder(object):
	def __init__(self, tfsession, scheme):
		if scheme == 'symmetric':
			inherited_classes = [general_hyper_parameters, symmetric_hyper_parameters,
					model_data, symmetric_training_model, symmetric_testing_model,
					model_trainer, model_builder, symmetric_model_tester]
		elif scheme == 'asymmetric':
			inherited_classes = [general_hyper_parameters, asymmetric_hyper_parameters,
					model_data, asymmetric_training_model, asymmetric_testing_model,
					model_trainer, model_builder, asymmetric_model_tester]
		else:
			inherited_classes = [general_hyper_parameters, asymmetric_hyper_parameters,
					model_data, hybrid_training_model, hybrid_testing_model, 
					model_trainer, model_builder, symmetric_model_tester]
		class model_engine(*inherited_classes,object):
			def __init__(self, inherited_classes, tfsession, scheme):
				self.tfsession = tfsession
				self.scheme = scheme	
				result_processor.start_time
				for inherited_classe in inherited_classes:
					inherited_classe.__init__(self)
				self.build_training_model()
				self.train()
				print('errors in training', len(self.errors['bob']),
				len(self.errors['eve']),
				len(self.errors['alan']))
				result_processor.process_uptime(self.scheme)
				result_processor.save_model(self.scheme, self.tfsession, self.model_saver, 'TRAINING')
				result_processor.process_results(self.scheme, self.errors, 'TRAINING',
				x_scale=self.hyper_parameters["epochs"]*self.hyper_parameters["iterations"],
				x_scale_caption=' iterations', y_scale_caption='decryption errors')
		
				self.build_testing_model()
				self.test()
				print('errors in testing', len(self.errors['bob']),
				len(self.errors['eve']),
				len(self.errors['alan']))
				result_processor.process_results(self.scheme, self.errors, 'TESTING',
				x_scale=self.hyper_parameters["epochs"]*self.hyper_parameters["iterations"],
				x_scale_caption=' iterations', y_scale_caption='decryption errors')
		modelEngine = model_engine(inherited_classes, tfsession, scheme)
				
		
