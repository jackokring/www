# SHELLINABOX_ARGS="-s '/:jackokring:jackokring:HOME:python www/siab.py'"
# >> /etc/default/shellinabox
# use curses module wrapper for terminal GUI
# requires .pem to avoid cert self sign error

# multiple routes beyond / and exit/error terminates shell connect
# $USER, https://localhost:4200/

from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()

    for i in range(0, 11):
        v = i-12
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))

    stdscr.refresh()
    stdscr.getkey()

wrapper(main)