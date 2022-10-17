#!/usr/bin/bash
# apply certbot to machine (with web server not running)

sudo apt update
sudo apt install -y python3 python3-venv libaugeas0 python-is-python3 openssl

sudo python -m venv /opt/certbot/
sudo /opt/certbot/bin/pip install --upgrade pip

sudo /opt/certbot/bin/pip install certbot

sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot

sudo certbot certonly --standalone

echo "0 0,12 * * * root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random() * 3600)' && sudo certbot renew -q" | sudo tee -a /etc/crontab > /dev/null

echo "0 0 1 * * root /home/$USER/www/cron-monthly.sh" | sudo tee -a /etc/crontab > /dev/null

cd ~/www
python -m venv venv