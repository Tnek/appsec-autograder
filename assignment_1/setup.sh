#!/bin/bash
apt-get update && apt-get install -y firefox python3 python3-pip curl
cp /autograder/source/geckodriver /usr/local/bin

#pip3 install -U pip
if [ -f "/autograder/source/requirements.txt" ]; then
    pip3 install -r /autograder/source/requirements.txt
else
    echo "FILE requirements.txt DOES NOT EXIST"
    pwd
    ls `pwd`
    exit 1
fi

