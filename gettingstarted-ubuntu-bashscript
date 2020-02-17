#!/bin/bash

## check for root permissions ##
if [ $USER = 'root' ]
then

## install prerequisites ##
apt-get install -y libc6
apt-get install -y libfreetype6
apt-get install -y fontconfig

## install git ##
apt-get install -y git

## create git working directory ##
mkdir /home/glasswall/Desktop/glasswall/
cd /home/glasswall/Desktop/glasswall

##
echo "Cloning the Glasswall libraries"

## clone into working directory ##
git clone https://github.com/filetrust/SDK-Evaluation-Version-2.x.git

## copy SDK into folders ##
ln -s /home/glasswall/Lib/libglasswall_core2.so /usr/lib/libglasswall_core2.so.2 && \
ln -s /home/glasswall/Lib/libQt5Concurrent.so /usr/lib/libQt5Concurrent.so.5 && \
ln -s /home/glasswall/Lib/libQt5Core.so /usr/lib/libQt5Core.so.5 && \
ln -s /home/glasswall/Lib/libquazip.so /usr/lib/libquazip.so.1 && \
ln -s /home/glasswall/Lib/libQt5Xml.so /usr/lib/libQt5Xml.so.5 && \
ln -s /home/glasswall/Lib/libicui18n.so /usr/lib/libicui18n.so.56 && \
ln -s /home/glasswall/Lib/libicuuc.so /usr/lib/libicuuc.so.56 && \
ln -s /home/glasswall/Lib/libicudata.so /usr/lib/libicudata.so.56 && \
ln -s /home/glasswall/Lib/libQt5Gui.so /usr/lib/libQt5Gui.so.5 && \
ldconfig /usr/lib

##
echo "The Glasswall Engine is ready"

##

else
		echo "##################"
        echo "Please run as root"
		echo "##################"
        exit 1
fi
