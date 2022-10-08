#!/usr/bin/bash

# install repos
sudo apt install apache2 php nodejs npm

# make an owner of the file structure
sudo chown -R $USER /var/www

# make git repository if possible
cd /var/www
git init

# make apache relaunch :80
sudo cp 000-default.conf /etc/apache2/sites-available
sudo a2ensite 000-default
sudo systemctl restart apache2

# start node :3000
cd node
npm install express jquery bootstrap underscore
node app.js

# python install :8000
# and a wolfram kernal :18000
# plus some local oomph via jax
pip install autograd wolframwebengine jax[cpu]
# full www directory. Not sutable for production
# and cgi-bin handler for localhost use
python3 -m http.server --cgi
# wolfram web engine licence (V13.1)
sudo cp secrets/LICENSE.txt /usr/local/Wolfram/WolframEngine/13.1
python3 -m wolframwebengine wl

