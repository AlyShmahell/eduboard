import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="neurencoder",
	version="1.0",
	author="Aly Shmahell",
	author_email="aly.shmahell@gmail.com",
	description="A small example package",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitlab.com/AlyShmahell/AlyShmahell-BachelorThesis",
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
	scripts=['extra-requirements.sh'],
	packages=setuptools.find_packages(),
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: Copyrights 2018 :: Aly Shmahell :: All Rights Reserved",
		"Operating System :: Ubuntu 16.04",
	),
)
