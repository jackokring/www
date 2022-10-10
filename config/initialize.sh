#!/usr/bin/bash

# it all happens here
cd /var/www

#update
gksudo apt update && apt upgrade -y

# install repos
sudo apt install -y apache2 php nodejs npm build-essential git

# make an owner of the file structure
sudo chown -R $USER /var/www

# add an easy desktop shortcut
# and make all config shell scripts executable
# change "server" to be unique 
chmod +x config/*.sh
desktop-file-install --dir=~/.local/share/applications config/server.desktop
update-desktop-database ~/.local/share/applications

# make git repository if possible
git init

# make apache relaunch :80
sudo cp 000-default.conf /etc/apache2/sites-available
sudo a2ensite 000-default
sudo systemctl restart apache2

# start node :3000
cd node
npm install express jquery bootstrap underscore browserify
node app.js&
cd ..

# python install AI tooling
pip install autograd wolframwebengine jax[cpu] mypy

# full www directory. Not sutable for production :8000
# and cgi-bin handler for localhost use
# this restriction is due to placement of document root and security
python3 -m http.server --cgi --bind 127.0.0.1&

# and a wolfram kernal :18000
# wolfram web engine licence (V13.1)
sudo cp secrets/LICENSE.txt /usr/local/Wolfram/WolframEngine/13.1
python3 -m wolframwebengine wl&

# so then launch browser default
xdg-open "http://localhost"