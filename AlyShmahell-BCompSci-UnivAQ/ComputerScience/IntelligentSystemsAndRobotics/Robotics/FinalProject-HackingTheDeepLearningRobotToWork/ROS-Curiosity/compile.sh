#!/bin/bash
cd build
cmake ..
make
cp ./devel/lib/curiosity/curiosity ../bin/curiosity
cd ..
rm -rf build -R
mkdir build

