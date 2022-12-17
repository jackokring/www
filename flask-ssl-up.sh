#!/bin/bash
# bring up flask

source config-env.sh

echo "SSL Server."
# so then launch browser default
# xdg-open "https://localhost"
python ssl-boot.py
