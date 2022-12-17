#!/bin/bash
# check source code

# python ok type check
mypy .

# and TypeScript here
# seems to be automatic vscode compile
#tsc

notify-send "Checked source"