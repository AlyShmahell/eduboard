#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Runs neurencoder as a standalone script for training and testing."""
__author__ = "Aly Shmahell"
__copyright__ = "Copyright 2018, Aly Shmahell"
__license__ = "All Rights Reserved"
__version__ = "1.0"
__maintainer__ = "Aly Shmahell"
__email__ = "aly.shmahell@gmail.com"
__status__ = "Git Tag"

from neurencoder.core_classes import *

def main():
	tf.logging.set_verbosity(tf.logging.INFO)
	config=tf.ConfigProto(log_device_placement=True)
	with tf.Session(config=config) as tfsession:
		neurencoder(tfsession)
		
		
if __name__ == '__main__':
	main()
