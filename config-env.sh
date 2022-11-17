# make sure dependancies are updated
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git

# enter directory just in case not there
cd ~/www

# activate virtual environment
source venv/bin/activate

# update pip
pip install --upgrade pip

# update all outdated packages
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

# install python packages on top
pip install autograd jax[cpu] mypy Flask pandas scikit-learn wheel build twine latexify-py

# make sure there's nothing running which is a duplicate
sudo killall --user $USER flask
sudo killall --user $USER ssl-boot.py

# set config information

