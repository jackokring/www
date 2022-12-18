#!/bin/bash
# check source code

# script directory
DIR=$( dirname -- "$0"; )
cd "$DIR"

# python ok type check
mypy .

# and TypeScript here
# seems to be automatic vscode compile
#tsc

notify-send "Checked source"