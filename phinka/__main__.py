# use phinka.sh script

# get version from module so only using pyproject.toml for version of __main__
from importlib.metadata import version

try:
    __version__ = version(__package__ or __name__)
except:
    __version__ = 'development-alpha-version'

# exception hook handler for supression of traceback in normal use
import sys

debug = False

def exception_handler(exception_type, exception, traceback):
    if debug:
        sys.__excepthook__(exception_type, exception, traceback)
    else:
        print('%s: %s' % (exception_type.__name__, exception))

sys.excepthook = exception_handler

# main
VERSION = __version__   # main version from pyproject.toml
HELP = 'Phinka tools for data processing'

import argparse
import phinka.blwz as blwz
import phinka.dx as dx

def resolve(args):
    """argument action resolver"""
    raise TypeError('you must supply a sub-command')

def main(parser: argparse.ArgumentParser):
    parser.add_argument('-v', '--version', action = 'version', version = '%(prog)s ' + VERSION)
    parser.add_argument('-d', '--debug', action = 'store_true', help = 'debug tracebacks')
    adder = parser.add_subparsers(help = 'sub-command')

    # blwz
    parser = adder.add_parser('blwz', help = blwz.HELP)
    parser.set_defaults(func = blwz.resolve)
    blwz.main(parser)

    # dx
    parser = adder.add_parser('dx', help = dx.HELP)
    parser.set_defaults(func = dx.resolve)
    dx.main(parser)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog = 'python -m phinka',
        description = HELP,
        epilog = 'Thanks.\nThe Management.')
    parser.set_defaults(func = resolve)
    main(parser)
    args = parser.parse_args()
    # is debug?
    if args.debug:
        debug = True
    args.func(args)
