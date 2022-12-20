#!/bin/bash
# monthly tasks

# update certbot for SSL
sudo /opt/certbot/bin/pip install --upgrade certbot

# script directory
DIR=$( dirname -- "$0"; )
cd "$DIR"

notify-send "phinka cron monthly complete"