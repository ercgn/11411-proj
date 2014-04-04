#!/bin/bash
#
# Installs the Python modules for the KenLM language model implementation.
#
# Run with sudo to install system-wide; otherwise installs for the current
# user only.
#
# Dependencies:
#  g++
#  pip (for system-wide install)

if [ $(id -u) -eq 0 ] ; then
    echo Installing KenLM system-wide...
    
    pip install https://github.com/kpu/kenlm/archive/master.zip
else
    echo Installing KenLM for user: $USER
    
    wget http://kheafield.com/code/kenlm.tar.gz
    tar -xzf kenlm.tar.gz
    cd kenlm
    python setup.py install --user
    cd ../
#    rm -rf kenlm/ kenlm.tar.gz
fi

exit 0

