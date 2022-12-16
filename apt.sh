#!/usr/bin/bash
# perform updates using apt
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git python3 python3-venv libaugeas0 python-is-python3 openssl libnotify-bin