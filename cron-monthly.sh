#!/bin/bash
# monthly tasks

# run as $USER
# don't config-env.sh as it is not command initiated, but monthly
# this means the $PATH is set via cron, and not all commands will work as expected
# but a logical directory is ~ and as might depend on interactive then

# update certbot for SSL
sudo /opt/certbot/bin/pip install --upgrade certbot

# .profile   echo $DBUS_SESSION_BUS_ADDRESS > ~/.dbus/bus
export DBUS_SESSION_BUS_ADDRESS=$(cat ~/.dbus/bus)
notify-send "phinka cron monthly complete"