#!/bin/sh
if ! type easy_install > /dev/null; then
    echo ""
    echo ""
    echo "############################################################"
    echo "# You'll need to enter your password to install Flask here #"
    echo "############################################################"
    sudo curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python
fi

export PYTHONPATH=$PYTHONPATH:~/python_packages
echo 'export PYTHONPATH=$PYTHONPATH:~/python_packages' >> ~/.bash_profile
mkdir -p ~/python_packages
easy_install --install-dir ~/python_packages flask
echo ""
echo ""
echo "#################################################################################"
echo "# Flask installed! Please close this terminal and open a new one to get started #"
echo "#################################################################################"
