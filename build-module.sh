#!/bin/bash

cd ~/www

# N.B. Might need ~/.local/ copy to ~/www/venv/
# It seems pip was in need of installing in the right place
# wirdness with /usr/bin/pip needed
# (venv) jackokring@penguin:~/www/venv/bin$ ln -s pip3 pip

# clear old dist files
rm -rf dist/*

# build python module phinka
python -m build

# place on PyPI
# Username: __token__
# Password: <API KEY>

# follow the PyPI $HOME/.pypirc advice
twine upload dist/*
notify-send "Built and uploaded Python module"