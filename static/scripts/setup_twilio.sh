#!/bin/sh
if ! type easy_install > /dev/null; then
    echo ""
    echo ""
    echo "############################################################"
    echo "# You'll need to enter your password to install Flask here #"
    echo "############################################################"
    sudo curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python
fi
easy_install --install-dir ~/python_packages twilio
