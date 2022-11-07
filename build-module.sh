#!/usr/bin/bash

# build python module phinka
python -m build

# place on PyPI
# Username: __token__
# Password: <API KEY>

# follow the PyPI $HOME/.pypirc advice
cd ~/www
twine upload dist/*
