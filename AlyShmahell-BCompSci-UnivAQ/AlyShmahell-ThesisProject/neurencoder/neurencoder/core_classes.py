# -*- coding: utf-8 -*-
"""The core classes of neurencoder."""
__author__ = "Aly Shmahell"
__copyright__ = "Copyright 2018, Aly Shmahell"
__license__ = "All Rights Reserved"
__version__ = "1.0"
__maintainer__ = "Aly Shmahell"
__email__ = "aly.shmahell@gmail.com"
__status__ = "Git Tag"

'''
' required python 3 builtin modules
'''
import json
import sys, os
from os.path import expanduser

'''
' required python 3 3rd-party modules
'''
import datetime
import tensorflow as tf
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import progressbar
import logging.config

'''
' optional own modules
'''
from neurencoder.helper_classes import *

'''
' neurencoder data paths initialization
'''
home_directory = expanduser("~")
neurencoder_data_home = home_directory + '/neurencoder-data/saved_model_data/'
if not os.path.exists(neurencoder_data_home):
	os.makedirs(neurencoder_data_home)
	
'''
' logger initialization
'''
logging_configuration_file = os.path.join(os.path.dirname(__file__), 'logging_config.json')
logging.config.dictConfig(json.load(open(logging_configuration_file)))
logger = logging.getLogger()


class general_hyper_parameters(object):

	def __init__(self):
		logger.info('%s class is initiated', 'general_hyper_parameters')
		super().__init__()
		hyper_parameters_file = os.path.join(os.path.dirname(__file__), 'hyper_parameters.json')
		self.hyper_parameters = json.load(open(hyper_parameters_file))
		'''
		' checking if the filter matrix shape and values are correct
		'''
		try:
			if np.shape(self.hyper_parameters['filters']) != (4, 3):
				raise ValueError(
				    'there is something wrong with filters\' shape inside hyper_parameters.json'
				)
			if np.array_equal(self.hyper_parameters['filters'], [[
			    self.hyper_parameters['filters'][0][0], 1,
			    self.hyper_parameters['filters'][0][2]
			], [
			    self.hyper_parameters['filters'][1][0],
			    self.hyper_parameters['filters'][0][2],
			    self.hyper_parameters['filters'][1][2]
			], [
			    self.hyper_parameters['filters'][2][0],
			    self.hyper_parameters['filters'][1][2],
			    self.hyper_parameters['filters'][2][2]
			], [
			    self.hyper_parameters['filters'][3][0],
			    self.hyper_parameters['filters'][2][2], 1
			]]) == False:
				raise ValueError(
				    'there is something wrong with filter values inside hyper_parameters.json'
				)
		except ValueError as e:
			logger.error(e)
			sys.exit()
			


class asymmetric_hyper_parameters(general_hyper_parameters):

	def __init__(self):
		logger.info('%s class is initiated', 'asymmetric_hyper_parameters')
		super().__init__()
		self.hyper_parameters['No_of_FC_Layers']['eve'] = 2 * (
		    self.hyper_parameters['No_of_FC_Layers']['alice'] +
		    self.hyper_parameters['No_of_FC_Layers']['bob'] +
		    self.hyper_parameters['No_of_FC_Layers']['pub_key_gen'] +
		    self.hyper_parameters['No_of_FC_Layers']['priv_key_gen'])
		self.hyper_parameters['No_of_FC_Layers'][
		    'alan'] = self.hyper_parameters['No_of_FC_Layers']['eve']


class symmetric_hyper_parameters(general_hyper_parameters):

	def __init__(self):
		logger.info('%s class is initiated', 'symmetric_hyper_parameters')
		super().__init__()
		self.hyper_parameters['No_of_FC_Layers'][
		    'eve'] = 2 * (self.hyper_parameters['No_of_FC_Layers']['alice'] +
		                  self.hyper_parameters['No_of_FC_Layers']['bob'])
		self.hyper_parameters['No_of_FC_Layers'][
		    'alan'] = self.hyper_parameters['No_of_FC_Layers']['eve']


class neurencoder_base(object):

	def __init__(self):
		logger.info('%s class is initiated', 'neurencoder_base')
		super().__init__()
		self.init_model_data()
		self.init_result_processor()

	'''
	' model data
	'''
	def init_model_data(self):
		self.placeholders = {
			'msg':
				tf.placeholder("float", [None, self.hyper_parameters["msg_len"]]),
			'key_seed':
				tf.placeholder("float",
							   [None, self.hyper_parameters["key_seed_len"]]),
			'encrypted_msg':
				tf.placeholder("float", [None, self.hyper_parameters["msg_len"]]),
			'priv_key':
				tf.placeholder("float",
							   [None, self.hyper_parameters["key_seed_len"]]),
			'pub_key':
				tf.placeholder("float",
							   [None, self.hyper_parameters["key_seed_len"]])
		}
		self.errors = {'bob': [], 'eve': [], 'alan': []}
		
	def reset_errors(self):
		logger.info('errors have been reset')
		self.errors = {'bob': [], 'eve': [], 'alan': []}
			
	'''
	' helper functions
	'''
	random_binary = lambda self, shape, dtype, partition_info=None:\
		(tf.random_uniform(shape, minval = 0, maxval = 2, dtype=dtype)*2-1)

	def generate_data(self, local_batch_size):
		return (np.random.randint(0, 2, size=(local_batch_size, self.hyper_parameters["msg_len"]))*2-1),\
            	(np.random.randint(0, 2, size=(local_batch_size, self.hyper_parameters["key_seed_len"]))*2-1)

	'''
	' model builder
	'''
	def build_net(self,
	              net_name,
	              net_input,
	              halved_first_layer_flag=False):
		if self.build_mode == 'training':
			self.weights = [
			    tf.get_variable(
			        net_name + "_w" + str(whichFCL),
			        [(self.hyper_parameters["key_seed_len"],
			          0)[halved_first_layer_flag == True and
			             whichFCL == 0] + self.hyper_parameters["msg_len"],
			         self.hyper_parameters["key_seed_len"] +
			         self.hyper_parameters["msg_len"]],
			        initializer=tf.contrib.layers.xavier_initializer())
			    for whichFCL in range(self.hyper_parameters["No_of_FC_Layers"][
			        net_name])
			]
		else:
			self.graph = tf.get_default_graph()
			self.weights = [
			    self.graph.get_tensor_by_name(net_name + "_w" + str(whichFCL) +
			                                  ":0") for whichFCL in
			    range(self.hyper_parameters["No_of_FC_Layers"][net_name])
			]
		fc_layer = tf.nn.sigmoid(tf.matmul(net_input, self.weights[0]))
		for i in range(1, self.hyper_parameters["No_of_FC_Layers"][net_name]):
			fc_layer = tf.nn.sigmoid(tf.matmul(fc_layer, self.weights[i]))
		hidden_layer = tf.expand_dims(fc_layer, 2)
		net = tf.squeeze(
		    self.build_4_1D_convolutions(hidden_layer, net_name))
		return net

	def build_4_1D_convolutions(self, hidden_layer, name):
		convolution_0 = tf.nn.leaky_relu(
		    self.build_1D_convolution(
		        hidden_layer,
		        self.hyper_parameters["filters"][0],
		        stride=1,
		        name=name + '_conv0'))
		convolution_1 = tf.nn.leaky_relu(
		    self.build_1D_convolution(
		        convolution_0,
		        self.hyper_parameters["filters"][1],
		        stride=2,
		        name=name + '_conv1'))
		convolution_2 = tf.nn.leaky_relu(
		    self.build_1D_convolution(
		        convolution_1,
		        self.hyper_parameters["filters"][2],
		        stride=1,
		        name=name + '_conv2'))
		convolution_3 = tf.nn.tanh(
		    self.build_1D_convolution(
		        convolution_2,
		        self.hyper_parameters["filters"][3],
		        stride=1,
		        name=name + '_conv3'))
		return convolution_3

	def build_1D_convolution(self, layer, filter_shape, stride,
	                         name):
		if self.build_mode == 'training':
			with tf.variable_scope(name):
				weight_filter = tf.get_variable(
				    'w',
				    shape=filter_shape,
				    initializer=tf.contrib.layers.xavier_initializer())
				return tf.nn.conv1d(
				    layer, weight_filter, stride, padding='SAME')
		else:
			weight_filter = self.graph.get_tensor_by_name(name + "/w:0")
			return tf.nn.conv1d(layer, weight_filter, stride, padding='SAME')
			
	'''
	' model trainer
	'''
	def run_training_model(self):
		tf.global_variables_initializer().run()
		self.model_saver = tf.train.Saver()
		#self.model_SummaryWriter = tf.summary.FileWriter(logdir = neurencoder_data_home + 'tensorboard-log', graph=tf.get_default_graph().as_graph_def())
		#self.dynamic_plot_init()
		for epoch in range(1, self.hyper_parameters["epochs"] + 1):
			msg_val, key_seed_val = self.generate_data(
			    local_batch_size=self.hyper_parameters["batch_size"])
			logger.info('training Alice, Bob - Epoch: %s', epoch)
			self.iterate('bob', msg_val, key_seed_val)
			logger.info('training Eve - Epoch: %s', epoch)
			self.iterate('eve', msg_val, key_seed_val)
			logger.info('training Alan - Epoch: %s', epoch)
			msg_val, key_seed_val = self.generate_data(
			    local_batch_size=self.hyper_parameters["batch_size"])
			self.iterate('alan', msg_val, key_seed_val)

	def iterate(self, network, msg_val, key_seed_val):
		self.progressbar_init(
		    steps=self.hyper_parameters["iterations"])
		for i in range(self.hyper_parameters["iterations"]):
			exercise = self.tfsession.run(
			    [self.optimizers[network], self.loss_functions[network][0]],
			    feed_dict={
			        self.placeholders['msg']: msg_val,
			        self.placeholders['key_seed']: key_seed_val
			    })
			self.errors[network].append(exercise[1])
			self.progressbar_update(i + 1)
			#self.dynamic_plot_update()
		self.progressbar_finish()
		
	def test_data_shape(self):
		msg_val, key_seed_val = self.generate_data(
			    local_batch_size=self.hyper_parameters["batch_size"])
		exercise = self.tfsession.run([self.networks['alice'], self.networks['bob'], self.networks['eve'], self.networks['alan']],
			    feed_dict={
			        self.placeholders['msg']: msg_val,
			        self.placeholders['key_seed']: key_seed_val
			    })
		logger.debug('alice\'s output shape: %s ', exercise[0].shape)
		logger.debug('bob\'s output shape: %s ', exercise[1].shape)
		logger.debug('eve\'s output shape: %s ', exercise[2].shape)
		logger.debug('alan\'s output shape: %s ', exercise[3].shape)

	'''
	' result processor
	'''
	def init_result_processor(self):
		self.plt_xScale = self.hyper_parameters["epochs"] * self.hyper_parameters["iterations"]
		self.plt_xScale_caption = str(self.plt_xScale) + ' iterations'
		self.plt_yScale_caption = 'decryption errors'
		self.model_data_subpath = neurencoder_data_home + datetime.datetime.now(
		).strftime("%Y-%m-%d-%H:%M:%S")
		os.makedirs(self.model_data_subpath)
		
	def progressbar_init(self, steps):
		self.current_progress_bar = progressbar.ProgressBar(
		    maxval=steps,
		    widgets=[
		        progressbar.Bar('+', '[', ']'), ' ',
		        progressbar.Percentage()
		    ])
		self.current_progress_bar.start()
	
	def progressbar_update(self, step):
		self.current_progress_bar.update(step)
	
	def progressbar_finish(self):
		self.current_progress_bar.finish()
		
	def dynamic_plot_init(self):
		pg.setConfigOption('background', 'w')
		pg.setConfigOption('foreground', 'k')
		self.win = pg.GraphicsWindow(title=tf.flags.FLAGS.scheme)
		pg.setConfigOptions(antialias=True)
		self.plotter = self.win.addPlot(title=self.build_mode)
		self.legend = pg.LegendItem()
		self.legend.setParentItem(self.plotter)
		self.curves = []
		rand_color_components = []
		for net_number, net_name in enumerate(self.errors):
			rand_color_component = np.random.randint(20, 255)
			while rand_color_component in [color_component+25 for color_component in rand_color_components]:
				rand_color_component = np.random.randint(20, 255)
			rand_color_components.append(rand_color_component)
			red = (1%(net_number+1) * rand_color_component) % 255
			green = (2%(net_number+1) * rand_color_component) % 255
			blue = (3%(net_number+1) * rand_color_component) % 255
			self.newPen = pg.mkPen(color=(red, green, blue), width=2)
			self.curves.append(self.plotter.plot(pen=self.newPen))
			self.legend.addItem(self.curves[len(self.curves) - 1], net_name)

	def dynamic_plot_update(self):
		pg.QtGui.QApplication.processEvents()
		for net_number, net_name in enumerate(self.errors):
			self.curves[net_number].setData(self.errors[net_name])

	def process_results(self):
		seaborn.set_style("whitegrid")
		legend = []
		for net_name in self.errors:
			plt.plot([epoch for epoch in range(1, (self.plt_xScale) + 1)],
			         self.errors[net_name])
			legend.append(net_name)
		plt.legend(legend)
		plt.xlabel(self.plt_xScale_caption + '\nUptime: ' +
		           str(datetime.datetime.now() - self.start_time))
		plt.ylabel(self.plt_yScale_caption)
		self.mode_data_relative_file_name = self.model_data_subpath + '/neurencoder-' + tf.flags.FLAGS.scheme + '-' + self.build_mode
		plt.savefig(self.mode_data_relative_file_name + '.svg')
		plt.show()

	def save_model(self):
		self.mode_data_relative_file_name = self.model_data_subpath + '/neurencoder-' + tf.flags.FLAGS.scheme + '-' + self.build_mode
		self.model_saver.save(self.tfsession,
		                      self.mode_data_relative_file_name + '-model')


class asymmetric_training_model(object):

	def __init__(self):
		logger.info('%s class is initiated', 'asymmetric_training_model')
		super().__init__()

	def build_training_model(self):
		self.networks = {}
		self.networks['pub_key_generator'] = self.build_net(
		    'pub_key_gen', self.placeholders['key_seed'],
		    True)
		self.networks['priv_key_generator'] = self.build_net(
		    'priv_key_gen', self.networks['pub_key_generator'], True)
		self.networks['alice'] = self.build_net(
		    'alice',
		    tf.concat(
		        [self.placeholders['msg'], self.networks['pub_key_generator']],
		        1), False)
		self.networks['bob'] = self.build_net(
		    'bob',
		    tf.concat(
		        [self.networks['alice'], self.networks['priv_key_generator']],
		        1),
		    False)

		self.networks['eve'] = self.build_net(
		    'eve',
		    tf.concat(
		        [self.networks['alice'], self.networks['pub_key_generator']],
		        1),
		    False)
		self.networks['alan'] = self.build_net(
		    'alan',
		    tf.concat(
		        [self.networks['alice'], self.networks['pub_key_generator']],
		        1), False)
		self.loss_functions = {
		    'bob': [
		        tf.reduce_mean(
		            tf.abs(self.placeholders['msg'] - self.networks['bob'])),
		        tf.reduce_mean(
		            tf.abs(self.placeholders['msg'] - self.networks['bob'])) +
		        (1. - tf.reduce_mean(
		            tf.abs(self.placeholders['msg'] - self.networks['eve'])))**
		        2.
		    ],
		    'eve': [
		        tf.reduce_mean(
		            tf.abs(self.placeholders['msg'] - self.networks['eve']))
		    ],
		    'alan': [
		        tf.reduce_mean(
		            tf.abs(self.placeholders['msg'] - self.networks['alan']))
		    ]
		}
		self.tf_trainable_variables = tf.trainable_variables()
		self.training_variables = {
		    'bob': [
		        var for var in self.tf_trainable_variables
		        if 'alice_' in var.name or 'bob_' in var.name or
		        'pub_key_gen' in var.name or 'priv_key_gen' in var.name
		    ],
		    'eve':
		    [var for var in self.tf_trainable_variables if 'eve_' in var.name],
		    'alan':
		    [var for var in self.tf_trainable_variables if 'alan_' in var.name]
		}
		'''
		' debugs training_variables
		'
		'''
		for net in self.training_variables:
			for var in self.training_variables[net]:
				logger.debug(var)
		''''''
		self.optimizers = {
		    'bob': [
		        tf.train.AdamOptimizer(
		            self.hyper_parameters["learning_rate"]).minimize(
		                self.loss_functions['bob'][1],
		                var_list=self.training_variables['bob'])
		    ],
		    'eve': [
		        tf.train.AdamOptimizer(
		            self.hyper_parameters["learning_rate"]).minimize(
		                self.loss_functions['eve'][0],
		                var_list=self.training_variables['eve'])
		    ],
		    'alan': [
		        tf.train.AdamOptimizer(
		            self.hyper_parameters["learning_rate"]).minimize(
		                self.loss_functions['alan'][0],
		                var_list=self.training_variables['alan'])
		    ]
		}


class asymmetric_testing_model(object):

	def __init__(self):
		logger.info('%s class is initiated', 'asymmetric_testing_model')
		super().__init__()

	def build_testing_model(self):
		self.networks['pub_key_generator'] = self.build_net(
		    'pub_key_gen', self.placeholders['key_seed'],
		    True)
		self.networks['priv_key_generator'] = self.build_net(
		    'priv_key_gen', self.placeholders['pub_key'],
		    True)
		self.networks['alice'] = self.build_net(
		    'alice',
		    tf.concat([self.placeholders['msg'], self.placeholders['pub_key']],
		              1), False)
		self.networks['bob'] = self.build_net(
		    'bob',
		    tf.concat([
		        self.placeholders['encrypted_msg'],
		        self.placeholders['priv_key']
		    ], 1),
		    False)

		self.networks['eve'] = self.build_net(
		    'eve',
		    tf.concat([
		        self.placeholders['encrypted_msg'], self.placeholders['pub_key']
		    ], 1),
		    False)
		self.networks['alan'] = self.build_net(
		    'alan',
		    tf.concat([
		        self.placeholders['encrypted_msg'], self.placeholders['pub_key']
		    ], 1),
		    False)
		    
		    
class asymmetric_model_tester(object):

	def __init__(self):
		logger.info('%s class is initiated', 'asymmetric_model_tester')
		super().__init__()

	def run_testing_model(self):
		self.reset_errors()
		self.model_saver = tf.train.Saver()
		#self.dynamic_plot_init()
		for epoch in range(1, self.hyper_parameters["epochs"] + 1):
			msg_val, key_seed_val = self.generate_data(
			    local_batch_size=self.hyper_parameters["batch_size"])
			logger.info('testing Key-Pair Generation - Epoch: %s', epoch)
			self.iterate_pub_key_generation(key_seed_val)
			self.iterate_priv_key_generation()
			logger.info('testing Alice - Epoch: %s', epoch)
			self.iterate_alice(msg_val)
			logger.info('testing Bob - Epoch: %s', epoch)
			self.iterate_decryptors('bob', msg_val, key_seed_val)
			logger.info('testing eve - Epoch: %s', epoch)
			self.iterate_decryptors('eve', msg_val, key_seed_val)
			logger.info('testing Alan - Epoch: %s', epoch)
			self.iterate_decryptors('alan', msg_val, key_seed_val)

	def iterate_pub_key_generation(self, key_seed_val):
		self.progressbar_init(steps=self.hyper_parameters["iterations"])
		for i in range(self.hyper_parameters["iterations"]):
			self.pub_key_val = self.tfsession.run(
			    self.networks['pub_key_generator'],
			    feed_dict={self.placeholders['key_seed']: key_seed_val})
			self.progressbar_update(i + 1)
			#self.dynamic_plot_update()
		self.progressbar_finish()

	def iterate_priv_key_generation(self):
		self.progressbar_init(
		    steps=self.hyper_parameters["iterations"])
		for i in range(self.hyper_parameters["iterations"]):
			self.priv_key_val = self.tfsession.run(
			    self.networks['priv_key_generator'],
			    feed_dict={self.placeholders['pub_key']: self.pub_key_val})
			self.progressbar_update(i + 1)
			#self.dynamic_plot_update()
		self.progressbar_finish()

	def iterate_alice(self, msg_val):
		self.progressbar_init(
		    steps=self.hyper_parameters["iterations"])
		for i in range(self.hyper_parameters["iterations"]):
			self.encrypted_msg_val = self.tfsession.run(
			    self.networks['alice'],
			    feed_dict={
			        self.placeholders['msg']: msg_val,
			        self.placeholders['pub_key']: self.pub_key_val
			    })
			self.progressbar_update(i + 1)
			#self.dynamic_plot_update()
		self.progressbar_finish()

	def iterate_decryptors(self, network, msg_val, key_seed_val):
		self.progressbar_init(
		    steps=self.hyper_parameters["iterations"])
		for i in range(self.hyper_parameters["iterations"]):
			test_results = self.tfsession.run(
			    self.loss_functions[network][0],
			    feed_dict={
			        self.placeholders['msg']: msg_val,
			        self.placeholders['pub_key']: self.pub_key_val,
			        self.placeholders['priv_key']: self.priv_key_val,
			        self.placeholders['encrypted_msg']: self.encrypted_msg_val,
			        self.placeholders['key_seed']: key_seed_val
			    })
			self.errors[network].append(test_results)
			self.progressbar_update(i + 1)
			#self.dynamic_plot_update()
		self.progressbar_finish()


class symmetric_training_model(object):

	def __init__(self):
		logger.info('%s class is initiated', 'symmetric_training_model')
		super().__init__()

	def build_training_model(self):
		self.networks = {}
		self.networks['alice'] = self.build_net(
		    'alice',
		    tf.concat([self.placeholders['msg'], self.placeholders['key_seed']],
		              1), False)
		self.networks['bob'] = self.build_net(
		    'bob',
		    tf.concat([self.networks['alice'], self.placeholders['key_seed']],
		              1), False)
		self.networks['eve'] = self.build_net(
		    'eve', self.networks['alice'], True)
		self.networks['alan'] = self.build_net(
		    'alan', self.networks['alice'], True)
		self.loss_functions = {
		    'bob': [
		        tf.reduce_mean(
		            tf.abs(self.placeholders['msg'] - self.networks['bob'])),
		        tf.reduce_mean(
		            tf.abs(self.placeholders['msg'] - self.networks['bob'])) +
		        (1. - tf.reduce_mean(
		            tf.abs(self.placeholders['msg'] - self.networks['eve'])))**
		        2.
		    ],
		    'eve': [
		        tf.reduce_mean(
		            tf.abs(self.placeholders['msg'] - self.networks['eve']))
		    ],
		    'alan': [
		        tf.reduce_mean(
		            tf.abs(self.placeholders['msg'] - self.networks['alan']))
		    ]
		}
		tf_trainable_variables = tf.trainable_variables()
		self.training_variables = {
		    'bob': [
		        var for var in tf_trainable_variables
		        if 'alice_' in var.name or 'bob_' in var.name
		    ],
		    'eve':
		    [var for var in tf_trainable_variables if 'eve_' in var.name],
		    'alan':
		    [var for var in tf_trainable_variables if 'alan_' in var.name]
		}
		'''
		' debugs training_variables
		'
		'''
		for net in self.training_variables:
			for var in self.training_variables[net]:
				logger.debug(var)
		''''''
		self.optimizers = {
		    'bob': [
		        tf.train.AdamOptimizer(
		            self.hyper_parameters["learning_rate"]).minimize(
		                self.loss_functions['bob'][1],
		                var_list=self.training_variables['bob'])
		    ],
		    'eve': [
		        tf.train.AdamOptimizer(
		            self.hyper_parameters["learning_rate"]).minimize(
		                self.loss_functions['eve'][0],
		                var_list=self.training_variables['eve'])
		    ],
		    'alan': [
		        tf.train.AdamOptimizer(
		            self.hyper_parameters["learning_rate"]).minimize(
		                self.loss_functions['alan'][0],
		                var_list=self.training_variables['alan'])
		    ]
		}


class symmetric_testing_model(object):

	def __init__(self):
		logger.info('%s class is initiated', 'symmetric_testing_model')
		super().__init__()

	def build_testing_model(self):
		self.networks['alice'] = self.build_net(
		    'alice',
		    tf.concat([self.placeholders['msg'], self.placeholders['key_seed']],
		              1), False)
		self.networks['bob'] = self.build_net(
		    'bob',
		    tf.concat([
		        self.placeholders['encrypted_msg'],
		        self.placeholders['key_seed']
		    ], 1),
		    False)
		self.networks['eve'] = self.build_net(
		    'eve', self.placeholders['encrypted_msg'], True)
		self.networks['alan'] = self.build_net(
		    'alan', self.placeholders['encrypted_msg'], True)
		    
		    
class symmetric_model_tester(object):

	def __init__(self):
		logger.info('%s class is initiated', 'symmetric_model_tester')
		super().__init__()

	def run_testing_model(self):
		self.reset_errors()
		self.model_saver = tf.train.Saver()
		#self.dynamic_plot_init()
		for epoch in range(1, self.hyper_parameters["epochs"] + 1):
			msg_val, key_seed_val = self.generate_data(
			    local_batch_size=self.hyper_parameters["batch_size"])
			logger.info('testing Alice - Epoch: %s', epoch)
			self.iterate_alice(msg_val, key_seed_val)
			logger.info('testing Bob - Epoch: %s', epoch)
			self.iterate_decryptors('bob', msg_val, key_seed_val)
			logger.info('testing Eve - Epoch: %s', epoch)
			self.iterate_decryptors('eve', msg_val, key_seed_val)
			logger.info('testing Alan - Epoch: %s', epoch)
			self.iterate_decryptors('alan', msg_val, key_seed_val)

	def iterate_alice(self, msg_val, key_seed_val):
		self.progressbar_init(
		    steps=self.hyper_parameters["iterations"])
		for i in range(self.hyper_parameters["iterations"]):
			self.encrypted_msg_val = self.tfsession.run(
			    self.networks['alice'],
			    feed_dict={
			        self.placeholders['msg']: msg_val,
			        self.placeholders['key_seed']: key_seed_val
			    })
			self.progressbar_update(i + 1)
			#self.dynamic_plot_update()
		self.progressbar_finish()

	def iterate_decryptors(self, network, msg_val, key_seed_val):
		self.progressbar_init(
		    steps=self.hyper_parameters["iterations"])
		for i in range(self.hyper_parameters["iterations"]):
			test_results = self.tfsession.run(
			    self.loss_functions[network][0],
			    feed_dict={
			        self.placeholders['msg']: msg_val,
			        self.placeholders['key_seed']: key_seed_val,
			        self.placeholders['encrypted_msg']: self.encrypted_msg_val
			    })
			self.errors[network].append(test_results)
			self.progressbar_update(i + 1)
			#self.dynamic_plot_update()
		self.progressbar_finish()


class hybrid_training_model(object):

	def __init__(self):
		logger.info('%s class is initiated', 'hybrid_training_model')
		super().__init__()

	def build_training_model(self):
		self.networks = {}
		self.networks['pub_key_generator'] = self.build_net(
		    'pub_key_gen', self.placeholders['key_seed'],
		    True)
		self.networks['priv_key_generator'] = self.build_net(
		    'priv_key_gen', self.networks['pub_key_generator'], True)
		self.networks['alice'] = self.build_net(
		    'alice',
		    tf.concat(
		        [self.placeholders['msg'], self.networks['pub_key_generator']],
		        1), False)
		self.networks['bob'] = self.build_net(
		    'bob',
		    tf.concat(
		        [self.networks['alice'], self.networks['priv_key_generator']],
		        1),
		    False)

		self.networks['eve'] = self.build_net(
		    'eve', self.networks['alice'], True)
		self.networks['alan'] = self.build_net(
		    'alan', self.networks['alice'], True)
		self.loss_functions = {
		    'bob': [
		        tf.reduce_mean(
		            tf.abs(self.placeholders['msg'] - self.networks['bob'])),
		        tf.reduce_mean(
		            tf.abs(self.placeholders['msg'] - self.networks['bob'])) +
		        (1. - tf.reduce_mean(
		            tf.abs(self.placeholders['msg'] - self.networks['eve'])))**
		        2.
		    ],
		    'eve': [
		        tf.reduce_mean(
		            tf.abs(self.placeholders['msg'] - self.networks['eve']))
		    ],
		    'alan': [
		        tf.reduce_mean(
		            tf.abs(self.placeholders['msg'] - self.networks['alan']))
		    ]
		}
		self.tf_trainable_variables = tf.trainable_variables()
		self.training_variables = {
		    'bob': [
		        var for var in self.tf_trainable_variables
		        if 'alice_' in var.name or 'bob_' in var.name or
		        'pub_key_gen' in var.name or 'priv_key_gen' in var.name
		    ],
		    'eve':
		    [var for var in self.tf_trainable_variables if 'eve_' in var.name],
		    'alan':
		    [var for var in self.tf_trainable_variables if 'alan_' in var.name]
		}
		'''
		' debugs training_variables
		'
		'''
		for net in self.training_variables:
			for var in self.training_variables[net]:
				logger.debug(var)
		''''''
		self.optimizers = {
		    'bob': [
		        tf.train.AdamOptimizer(
		            self.hyper_parameters["learning_rate"]).minimize(
		                self.loss_functions['bob'][1],
		                var_list=self.training_variables['bob'])
		    ],
		    'eve': [
		        tf.train.AdamOptimizer(
		            self.hyper_parameters["learning_rate"]).minimize(
		                self.loss_functions['eve'][0],
		                var_list=self.training_variables['eve'])
		    ],
		    'alan': [
		        tf.train.AdamOptimizer(
		            self.hyper_parameters["learning_rate"]).minimize(
		                self.loss_functions['alan'][0],
		                var_list=self.training_variables['alan'])
		    ]
		}


class hybrid_testing_model(object):

	def __init__(self):
		logger.info('%s class is initiated', 'hybrid_testing_model')
		super().__init__()

	def build_testing_model(self):
		self.networks['alice'] = self.build_net(
		    'alice',
		    tf.concat([self.placeholders['msg'], self.placeholders['key_seed']],
		              1), False)
		self.networks['bob'] = self.build_net(
		    'bob',
		    tf.concat([
		        self.placeholders['encrypted_msg'],
		        self.placeholders['key_seed']
		    ], 1),
		    False)
		self.networks['eve'] = self.build_net(
		    'eve', self.placeholders['encrypted_msg'], True)
		self.networks['alan'] = self.build_net(
		    'alan', self.placeholders['encrypted_msg'], True)

			
class neurencoder(object):

	def __init__(self, tfsession):
		'''
		' This is where the neurencoder execution tree root is
		'''
		logger.info('%s class is initiated', 'neurencoder')
		tf.flags.DEFINE_string('scheme', 'symmetric', 'chooses an encryption scheme, default: symmetric')
		if tf.flags.FLAGS.scheme == 'symmetric':
			inherited_classes = [symmetric_model_tester, symmetric_testing_model,
					symmetric_training_model, neurencoder_base, 
					symmetric_hyper_parameters]
		elif tf.flags.FLAGS.scheme == 'asymmetric':
			inherited_classes = [asymmetric_model_tester, asymmetric_testing_model,
					asymmetric_training_model, neurencoder_base, 
					asymmetric_hyper_parameters]
		elif tf.flags.FLAGS.scheme == 'hybrid':
			inherited_classes = [symmetric_model_tester, hybrid_testing_model,
					hybrid_training_model, neurencoder_base, 
					asymmetric_hyper_parameters]
		else:
			sys.exit('choose one shceme, and one scheme only: symmetric (default), asymmetric, hybrid')
		class model_engine(*inherited_classes,object):
			def __init__(self, tfsession):
				super().__init__()
				logger.info('Method Resolution Order:\n%s',np.array([x.__name__ for x in self.__class__.__mro__]))
				logger.info('%s class is initiated', 'model_engine')
				self.tfsession = tfsession
				self.start_time = datetime.datetime.now()
				self.build_mode = 'training'
				self.build_training_model()
				self.run_training_model()
				#self.test_data_shape()
				self.process_results()
				self.save_model()
				self.start_time = datetime.datetime.now()
				self.build_mode = 'testing'
				self.build_testing_model()
				self.run_testing_model()
				#self.test_data_shape()
				self.process_results()
				self.save_model()
		modelEngine = model_engine(tfsession)
