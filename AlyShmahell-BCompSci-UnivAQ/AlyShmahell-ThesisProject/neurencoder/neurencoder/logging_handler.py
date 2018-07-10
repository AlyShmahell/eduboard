# -*- coding: utf-8 -*-
"""a custom file handler for logging, to be used internally in the neurencoder project."""
__author__ = "Aly Shmahell"
__copyright__ = "Copyright © 2018, Aly Shmahell"
__license__ = "All Rights Reserved"
__version__ = "TDPR1"
__maintainer__ = "Aly Shmahell"
__email__ = "aly.shmahell@gmail.com"
__status__ = "Thesis Defense PreRelease"

import errno
import os
from os.path import expanduser
import logging

class file_handler(logging.handlers.RotatingFileHandler):

	def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding='utf-8', delay=0):
		log_path = expanduser("~") + '/neurencoder-data' + '/log'
		if not os.path.exists(log_path):
			os.makedirs(log_path)
		log_path += '/'
		logging.handlers.RotatingFileHandler.__init__(self, log_path + filename, mode, maxBytes, backupCount, encoding, delay)
		
	def emit(self, record):
		try:
			if logging.handlers.RotatingFileHandler.shouldRollover(self, record):
				logging.handlers.RotatingFileHandler.doRollover(self)
			logging.FileHandler.emit(self, record)
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			logging.handlers.RotatingFileHandler.handleError(self, record)
