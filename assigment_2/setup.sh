#!/bin/bash
apt-get update && apt-get install -y firefox python3 python3-pip curl
cp geckodriver /usr/local/bin

#pip3 install -U pip
pip3 install -r /autograder/source/requirements.txt
