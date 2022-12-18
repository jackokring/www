#!/bin/bash
# monthly tasks

# update certbot for SSL
/opt/certbot/bin/pip install --upgrade certbot

# script directory
DIR=$( dirname -- "$0"; )
cd "$DIR"

./notify-as-user.sh "phinka cron monthly complete"