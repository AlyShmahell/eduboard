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
		self.hyper_parameters['No_of_FC_Layers']['alan'] = self.hyper_parameters['No_of_FC_Layers']['eve']
					
							 		
class symmetric_hyper_parameters(general_hyper_parameters, object):

	def __init__(self):
		super(symmetric_hyper_parameters ,self).__init__()
		self.hyper_parameters['No_of_FC_Layers']['eve'] = 2*(self.hyper_parameters['No_of_FC_Layers']['alice']+
							 		self.hyper_parameters['No_of_FC_Layers']['bob'])
		self.hyper_parameters['No_of_FC_Layers']['alan'] = self.hyper_parameters['No_of_FC_Layers']['eve']


class model_builder(general_hyper_parameters, object):

	def __init(self):
		super(model_builder, self).__init__()
		
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
				'eve': [],
				'alan': []
				}
		
	def reset_errors(self):
		self.errors = {
				'bob': [],
				'eve': [],
				'alan': []
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
		self.alan = self.build_net('alan', tf.concat([self.alice,self.pub_key_generator], 1), 
							self.hyper_parameters["No_of_FC_Layers"]['eve'])
		self.loss_functions = {
					'bob': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.bob)),
						tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.bob))
						 + (1. - tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.eve))) ** 2.],
					'eve': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.eve))],
					'alan': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.alan))]
					}
		self.tf_trainable_variables = tf.trainable_variables()
		self.training_variables = {
					'bob' : [var for var in self.tf_trainable_variables if 'alice_' in var.name or 'bob_' in var.name],
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
				
				
class symmetric_model(symmetric_hyper_parameters, model_builder, model_data, object):

	def __init__(self):
		super(symmetric_model, self).__init__()
		
	def build_model(self):
		self.alice = self.build_net('alice', 
					tf.concat([self.placeholders['msg'], self.placeholders['key_seed']],1), self.hyper_parameters["No_of_FC_Layers"]['alice'])
		self.bob = self.build_net('bob', tf.concat([self.alice, self.placeholders['key_seed']],1), self.hyper_parameters["No_of_FC_Layers"]['bob'])
		self.eve = self.build_net('eve', self.alice, self.hyper_parameters["No_of_FC_Layers"]['eve'], True)
		self.alan = self.build_net('alan', self.alice, self.hyper_parameters["No_of_FC_Layers"]['eve'], True)
		self.loss_functions = {
					'bob': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.bob)),
						tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.bob))
						 + (1. - tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.eve))) ** 2.],
					'eve': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.eve))],
					'alan': [tf.reduce_mean(tf.abs(self.placeholders['msg'] - self.alan))]
					}
		tf_trainable_variables = tf.trainable_variables()
		self.training_variables = {
					'bob' : [var for var in tf_trainable_variables if 'alice_' in var.name or 'bob_' in var.name],
					'eve': [var for var in tf_trainable_variables if 'eve_' in var.name],
					'alan': [var for var in tf_trainable_variables if 'alan_' in var.name]
					}
		self.optimizers = {
					'bob': [tf.train.AdamOptimizer(self.hyper_parameters["learning_rate"]).minimize(
						self.loss_functions['bob'][1], var_list=self.training_variables['bob'])],
					'eve': [tf.train.AdamOptimizer(self.hyper_parameters["learning_rate"]).minimize(
						self.loss_functions['eve'][0], var_list=self.training_variables['eve'])],
					'alan': [tf.train.AdamOptimizer(self.hyper_parameters["learning_rate"]).minimize(
						self.loss_functions['alan'][0], var_list=self.training_variables['alan'])]
					}
		

class model_trainer(model_builder, object):

	def __init__(self):
		super(model_trainer, self).__init__()
		
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
			self.iterate('alan', msg_val, key_seed_val)
		
	def iterate(self, network, msg_val, key_seed_val):
		iteration_progressbar = result_processor.progress_bar(steps=self.hyper_parameters["iterations"])
		for i in range(self.hyper_parameters["iterations"]):
			exercise = self.tfsession.run(
						[self.optimizers[network], self.loss_functions[network][0]],
						feed_dict={self.placeholders['msg']: msg_val, self.placeholders['key_seed']: key_seed_val})
			self.errors[network].append(exercise[1])
			iteration_progressbar.update(i+1)
		iteration_progressbar.finish()


class result_processor:

	start_time = datetime.datetime.now()
	def process_uptime(scheme):
		uptime = datetime.datetime.now() - result_processor.start_time
		print('Uptime: '+str(uptime))
		with open('./saved_model_data/neurencoder-'+scheme+'-Uptime-'+datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), "w") as uptime_outfile:
			uptime_outfile.write(str(uptime))
			
	def process_results(scheme, errors, x_scale, x_scale_caption, y_scale_caption, which_result):
		seaborn.set_style("whitegrid")
		legend = []
		for net_name in errors:
			pyplot.plot([epoch for epoch in range(1, (x_scale)+1)], errors[net_name])
			legend.append(net_name)
		pyplot.legend(legend)
		pyplot.xlabel(str(x_scale)+x_scale_caption)
		pyplot.ylabel(y_scale_caption)
		pyplot.savefig('./saved_model_data/neurencoder-'+scheme+'-'+which_result+'-plot_figure-'+datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")+'.svg')
		pyplot.show()
		
	def save_model(scheme, tfsession, model_saver): 
		model_saver.save(tfsession, './saved_model_data/neurencoder-'+scheme+'-model-'+datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"));
	
	class progress_bar(object):
	
		def __init__(self, steps):
			self.current_progress_bar = progressbar.ProgressBar(maxval=steps, widgets=[progressbar.Bar('+', '[', ']'), ' ', progressbar.Percentage()])
			self.current_progress_bar.start()
			
		def update(self, step):
			self.current_progress_bar.update(step)
			
		def finish(self):
			self.current_progress_bar.finish()
		
		
class neurencoder(symmetric_model, asymmetric_model, model_trainer, object):
	def __init__(self, tfsession, scheme):
		self.tfsession = tfsession
		self.scheme = scheme
		result_processor.start_time
		model_trainer.__init__(self)
		if self.scheme == 'symmetric':
			symmetric_model.__init__(self)
		else:
			asymmetric_model.__init__(self)
		self.build_model()
		self.train()
		result_processor.process_uptime(self.scheme)
		result_processor.save_model(self.scheme, self.tfsession, self.model_saver)
		result_processor.process_results(self.scheme, self.errors, x_scale=self.hyper_parameters["epochs"]*self.hyper_parameters["iterations"], x_scale_caption=' iterations', y_scale_caption='decryption errors', which_result='TRAINING')

