#!/bin/bash
# Used for prepare evaluator environment
# Since the evaluator base image is already built, this file won't be used

su - root
cd /
mkdir "/Temp"

# wget won't be installed when linux is packaged in a minimal way
yum -y install wget


yum groupinstall "Development tools"
install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel

# .c, .c++
yum install -y gcc gcc-c++
# .py
wget https://www.python.org/ftp/python/3.7.5/Python-3.7.5.tgz
tar -zxvf Python-3.7.5.tgz
mkdir /usr/lib/python3.7.5
cd /Python-3.7.5 || exit

./configure --prefix=/usr/lib/python3.7.5
make && make install

# .java
yum install -y java-1.8.0-openjdk*



