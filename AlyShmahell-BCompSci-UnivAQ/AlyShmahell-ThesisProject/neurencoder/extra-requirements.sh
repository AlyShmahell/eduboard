#!/bin/bash

	# install cuda toolkit and nvidia drivers
	bash -c "echo 'deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64 /' > /etc/apt/sources.list.d/cuda.list"
	sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
	sudo apt update
	sudo apt install nvidia-390 nvidia-390-dev cuda-9-0 nvidia-cuda-dev nvidia-cuda-toolkit
	
        
        # install cuDNN, obtained from : https://developer.nvidia.com/rdp/cudnn-download, after agreeing to the Software License Agreement
	sudo dpkg -i ./third-party/NVIDIA/cuDNN/libcudnn7_7.0.5.15-1+cuda9.1_amd64.deb
	sudo dpkg -i ./third-party/NVIDIA/cuDNN/libcudnn7-dev_7.0.5.15-1+cuda9.1_amd64.deb
	sudo dpkg -i ./third-party/NVIDIA/cuDNN/libcudnn7-doc_7.0.5.15-1+cuda9.1_amd64.deb
	
	
	# install pip, python-dev
	sudo apt install python-pip python-software-properties python-dev python3-pip python3-software-properties python3-dev
	# setup environment variables
	export PATH=/usr/local/cuda-9.0/bin${PATH:+:${PATH}}
	export LD_LIBRARY_PATH=/usr/local/cuda-9.0/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-9.0/extras/CUPTI/lib64
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/extras/CUPTI/lib64
        export CUDA_HOME=/usr/local/cuda-9.0
	# install numpy, matplot
	sudo pip3 install --no-cache-dir numpy matplotlib
	sudo pip2 install --no-cache-dir numpy matplotlib
	# install jupyter
	sudo pip3 install --no-cache-dir jupyter
	sudo pip2 install --no-cache-dir jupyter
	# install tensorflow, seaborn
	sudo pip3 install --no-cache-dir seaborn
	sudo pip3 install --no-cache-dir tensorflow-gpu
	sudo pip2 install --no-cache-dir seaborn
	sudo pip2 install --no-cache-dir tensorflow-gpu
