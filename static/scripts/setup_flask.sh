#!/bin/sh
export PYTHONPATH=$PYTHONPATH:~/python_packages
echo 'export PYTHONPATH=$PYTHONPATH:~/python_packages' >> ~/.bash_profile
mkdir -p ~/python_packages
easy_install --install-dir ~/python_packages flask
echo -e "\[\033[33m\]Flask installed! Please close this terminal and open a new one to get started.\[\033[0m\]"
