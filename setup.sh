#!/bin/bash
apt-get update && apt-get install -y firefox python3 python3-pip

pip3 install -U pip
pip install -r requirements.txt

