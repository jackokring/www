# make sure dependancies are updated
source apt.sh

# enter directory just in case not there
cd ~/www

# activate virtual environment
source venv/bin/activate

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