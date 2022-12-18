#!/bin/bash
# monthly tasks

# update certbot for SSL
/opt/certbot/bin/pip install --upgrade certbot

$( dirname -- "$0"; )/notify-as-user.sh "phinka cron monthly complete"