#!/usr/bin/bash
# check source code

# all shell scripts should be executable
chmod +x *.sh

# best done with shell script running module
#chmod +x phinka/phinka.py

# python ok type check
mypy .

# and TypeScript here
# seems to be automatic vscode compile
#tsc

notify-send "Checked source"