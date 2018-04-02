#!/bin/bash

	# install python pip
	sudo apt install python-pip python-software-properties
	# install required pip packages (tensorflow, jupyter,...etc)
	echo "installing scipy, numpy, matplotlib, pyqt5, pycuda, theano, lasagne..."
	sudo pip3 install sympy scipy numpy matplotlib pyqt5 pycuda
	sudo pip2 install sympy scipy numpy matplotlib pyqt5 pycuda
	sudo pip2 install --upgrade https://github.com/Theano/Theano/archive/master.zip
	sudo pip3 install --upgrade https://github.com/Theano/Theano/archive/master.zip
	sudo pip3 install --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip
	sudo pip2 install --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip
	echo "installing jupyter"
	sudo pip3 install jupyter
	sudo pip2 install jupyter
	echo "installing tensorflow..."
	sudo pip3 install seaborn
	sudo pip3 install https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.4.0-cp35-cp35m-linux_x86_64.whl
	sudo pip2 install seaborn
	sudo pip2 install https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.6.0-cp27-none-linux_x86_64.whl

	# taken from https://docs.docker.com/install/linux/docker-ee/ubuntu/ with some modifications
	# remove old versions of docker
	sudo apt-get remove docker docker-engine docker-ce docker.io
	sudo apt install linux-image-extra-$(uname -r) linux-image-extra-virtual apt-transport-https ca-certificates software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo apt-key fingerprint 0EBFCD88
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
	sudo apt update
	sudo apt install docker-ce
	sudo groupadd docker
	sudo usermod -aG docker $USER
	# install cuda toolkit and nvidia drivers
	wget "http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.1.85-1_amd64.deb"
	sudo dpkg -i cuda-repo-ubuntu1604_9.1.85-1_amd64.deb
	sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
	sudo apt update
	sudo apt install nvidia-390 nvidia-390-dev cuda nvidia-cuda-dev nvidia-cuda-toolkit 

	# taken from https://github.com/NVIDIA/nvidia-docker without modification
	# If you have nvidia-docker 1.0 installed: we need to remove it and all existing GPU containers
	docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f
	sudo apt-get purge -y nvidia-docker
	# Add the package repositories
	curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
	  sudo apt-key add -
	distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
	curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
	  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
	sudo apt-get update
	# Install nvidia-docker2 and reload the Docker daemon configuration
	sudo apt-get install -y nvidia-docker2
	sudo pkill -SIGHUP dockerd
	# Test nvidia-smi with the latest official CUDA image
	docker run --runtime=nvidia --rm nvidia/cuda nvidia-smi
