import platform
import re
import sys
import subprocess

from setuptools import Extension, setup

if sys.version_info < (3, 5):
	raise Exception('Python 2.7 is not supported.')

with open('README.md', 'r') as doc:
	long_description = doc.read()
	
with open('LICENSE', 'r') as legal:
	license = legal.read()

setup(
	name='neurencoder',
	version='1.0',
	author='Aly Shmahell',
	author_email='aly.shmahell@gmail.com',
	description='Hyper Heuristic Cryptography with Mixed Adversarial Nets',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://gitlab.com/AlyShmahell/AlyShmahell-BachelorThesis',
	license=license,
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
	scripts=['neurencoder_extra_requirements'],
	entry_points = {
		'console_scripts': ['neurencoder=neurencoder.executer:main'],
      }
)
