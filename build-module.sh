#!/usr/bin/bash

cd ~/www

# clear old dist files
rm -rf dist/*

# build python module phinka
python -m build

# place on PyPI
# Username: __token__
# Password: <API KEY>

# follow the PyPI $HOME/.pypirc advice
twine upload dist/*
