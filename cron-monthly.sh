#!/bin/bash
# monthly tasks

# run as $USER
# don't config-env.sh as it is not command initiated, but monthly
# this means the $PATH is set via cron, and not all commands will work as expected
# but a logical directory is ~ and as might depend on interactive then
cd ~

# update certbot for SSL
sudo /opt/certbot/bin/pip install --upgrade certbot

notify-send "phinka cron monthly complete"