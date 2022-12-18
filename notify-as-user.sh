#!/bin/bash
# any user in directory (including systemd etc.)
# might be useful to place the following in a convienient .bashrc
# echo $USER > username.txt
U=`cat username.txt`
/bin/bash -c "su $U; notify-send $1"