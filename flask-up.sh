#!/usr/bin/bash
# bring up flask

# make sure dependancies are updated
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git

# activate virtual environment
source venv/bin/activate

# update pip
pip install --upgrade pip

# update all outdated packages
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

# install python packages on top
pip install autograd jax[cpu] mypy Flask pandas scikit-learn

# get config information
source config-env.sh

if [[ -n $DEBUG ]]
then
    echo "DEBUG Server."
    # so then launch browser default
    xdg-open "http://localhost:1313"
    # start non secure debug server (keep log open)
    flask --debug run
else
    echo "SSL Server."
    # so then launch browser default
    xdg-open "https://localhost"
    python ssl-boot.py&
fi

