## Hacking the Deep Learning Robot (to work)

in order to control the kokubi base from within the laptop, one only needs the minimal kokubi installation, as portrayed and explained on this page:  
http://yujinrobot.github.io/kobuki/doxygen/enInstallationLinuxGuide.html    

however, if you're on Ubuntu 14.04, you might find it a bit tedious, since there are some things missing in your operating system.  

now I have updated the official tutorial to work with Ubuntu 14.04 as following:  

install the required libraries:  

sudo apt-get install python-pip libftdi-dev cmake python-empy python-nose python-setuptools build-essential  
sudo pip install wstool catkin-pkg

now compile from source as follows:  
```bash
mkdir ~/kobuki_core  
wstool init -j5 ~/kobuki_core/src https://raw.github.com/yujinrobot/kobuki_core/hydro/kobuki_core.rosinstall  
cd ~/kobuki_core  
export PATH=~/kobuki_core/src/catkin/bin/:${PATH}  
catkin_make  
cd build; make install  
```
finally, test your installation, by connecting to kokubi base, then running the following commands on your ubuntu computer:  
```bash
export LD_LIBRARY_PATH=~/kobuki_core/install/lib  
~/kobuki_core/install/lib/kobuki_driver/demo_kobuki_simple_loop  
```

