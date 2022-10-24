#!/usr/bin/bash
# bring up flask

source config-env.sh

echo "DEBUG Server."
# so then launch browser default
xdg-open "http://localhost:1313"
# start non secure debug server (keep log open)
flask --debug run
