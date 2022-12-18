#!/bin/bash
# allow bootstrap config
# make sure dependancies are updated
# perform updates using apt
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git python3 python3-venv libaugeas0 python-is-python3 openssl libnotify-bin xdotool

# enter directory just in case not there
if [ ! -d "~/www" ]; then
    # clone repository without secrets
    cd ~
    git clone https://github.com/jackokring/www.git
fi
cd ~/www
# all shell scripts should be executable
chmod +x *.sh
# might be useful
echo $USER > username.txt

if [ ! -d "venv/bin" ]; then
    # make virtual environment called venv
    python -m venv venv
fi

# activate virtual environment
source venv/bin/activate

# set PATH so it includes bin if it exists
if [ -d "$HOME/www/bin" ] ; then
    PATH="$HOME/www/bin:$PATH"
    chmod -R +x "$HOME/www/bin"
fi

# N.B. (venv) ~/www/venv/bin$ ln -s pip3 pip
# seems /usr/bin/pip goes for ~/.local installing
# ln -s venv/bin/pip3 venv/bin/pip

# update pip
pip3 install --upgrade pip

# update all outdated packages
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

# install python packages on top
pip install autograd jax[cpu] mypy Flask pandas scikit-learn wheel build twine latexify-py lovely-tensors

# dagshub
pip install dvc

# make sure there's nothing running which is a duplicate
sudo killall --user $USER flask
sudo killall --user $USER ssl-boot.py

# set config information

notify-send "Environment configured"