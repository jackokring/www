#!/bin/bash
# allow bootstrap config
# curl -L https://raw.githubusercontent.com/jackokring/www/master/config-env.sh > install.sh
# bash install.sh

# script directory
DIR=$( dirname -- "$0"; )
# "-bash" from | bash is not a proper directory
cd "$DIR"

# enter directory just in case not there
if [ ! -d "www" ]; then
    # clone repository without secrets (in home ... for curl?)
    git clone https://github.com/jackokring/www.git
    cd www
fi

# all shell scripts should be executable
chmod +x *.sh

if [ ! -d "venv/bin" ]; then
    # make virtual environment called venv
    python -m venv venv
fi

# activate virtual environment
source venv/bin/activate

# set PATH so it includes bin if it exists
if [ -d "$DIR/bin" ] ; then
    # double brakets suspends many shell operators like >, &&, * ... allowing logic and matching
    [[ ":$PATH:" != *":$DIR/bin:"* ]] && PATH="$DIR/bin:$PATH"
    chmod -R +x "$DIR/bin"
fi

# check time net efficiency
NS=$(date +%s)
if [ ! -f "sec.txt"] ; then
    echo 0 > sec.txt
fi

OLD=$(cat sec.txt)
NET=$(($NS - $OLD))

# step frame
echo $NS > sec.txt

# half hour
if (( $NET > 30 * 60 )) ; then

# make sure dependancies are updated
# perform updates using apt
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git python3 python3-venv 
sudo apt install -y libaugeas0 python-is-python3 openssl libnotify-bin xdotool
sudo apt install -y cron nano libgl1-mesa-glx libegl1-mesa
sudo apt install -y shellinabox imagemagick chafa

# N.B. (venv) ~/www/venv/bin$ ln -s pip3 pip
# seems /usr/bin/pip goes for ~/.local installing
# ln -s venv/bin/pip3 venv/bin/pip

# update pip
pip install --upgrade pip

# update all outdated packages (dependancy errors)
# pip list -o | cut -f1 -d' ' | tr " " "\n" | awk '{if(NR>=3)print}' | cut -d' ' -f1 | xargs -n1 pip install -U 
# check and downgrade
# pip check | awk '{print $1}' | xargs pip install --upgrade


# install python packages on top
pip install autograd jax[cpu] mypy Flask pandas scikit-learn wheel build twine
pip install markdown latexify-py lovely-tensors jupyter pytest
pip install chafa.py sympy

# dagshub
pip install dvc

# end net update limiter
echo "In 'nano ~/.profile' add once 'echo \$DBUS_SESSION_BUS_ADDRESS > ~/.dbus/bus' for notifications."
echo "In 'sudo nano /etc/crontab' add once before jobs 'MAILTO=\"\"' for no cron emails."
fi

# make sure there's nothing running which is a duplicate
sudo killall --user $USER flask
sudo killall --user $USER ssl-boot.py

# set config information

notify-send "Environment configured"
