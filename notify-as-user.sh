#!/bin/bash
# any user in directory (including systemd etc.)
# might be useful to place the following in a convienient .bashrc
# echo $USER > username.txt
# $( dirname -- "$0"; ) might be useful to reference this script
U=$( cat username.txt )
/bin/bash -c "su $U; notify-send $1"