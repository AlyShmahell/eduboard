import platform
import re
import sys

from setuptools import Extension, setup

if sys.version_info < (3, 5):
	raise Exception('Only Python 3.5 is supported.')
	
with open('LICENSE', 'r') as legal:
	license = " ".join(line.strip() for line in legal)

setup(
	name='neurencoder',
	version='TDPR1',
	author='Aly Shmahell',
	author_email='aly.shmahell@gmail.com',
	description='Hyper Heuristic Cryptography with Mixed Adversarial Nets',
	license=license,
	url='https://gitlab.com/AlyShmahell/AlyShmahell-Thesis',
	packages=['neurencoder'],
	install_requires=[
		'tensorflow-gpu>=1.8.0',
		'numpy>=1.14.2',
		'progressbar2>=3.37.1',
		'matplotlib>=2.2.2',
		'seaborn>=0.8.1',
		'pyqtgraph>=0.10.0'
		'datetime>=4.2'
	],
	platforms=['Ubuntu 16.04'],
	scripts=['neurencoder-extra-requirements'],
	entry_points = {
		'console_scripts': ['neurencoder=neurencoder.executer:main'],
      },
      classifiers=[
		'Development Status :: Thesis Defense PreRelease',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'Intended Audience :: Academic Researchers',
		'Intended Audience :: Industry Researchers',
		'Programming Language :: Python :: 3 :: 5',
		'Topic :: Artificial Intelligence :: Adeversarial Neural Networks',
		'Topic :: Artificial Intelligence :: Convolutional Neural Networks',
		'Topic :: Artificial Intelligence :: Transfer Learning',
		'Topic :: Cyrptology :: Symmetric Cryptography',
		'Topic :: Cyrptology :: Asymmetric Cryptography',
		'Topic :: Cyrptology :: Hybrid Cryptography',
		'Usage :: Standalone :: neurencoder -scheme [symmetric, asymmetric, hybrid]',
		'Usage :: Library :: from neurencoder import *',
	],
)
