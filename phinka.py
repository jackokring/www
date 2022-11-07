#!/usr/bin/python
# hash bang python script







# main
VERSION = '1.0.0'   # main version
HELP = 'Phinka tools for data processing'

import argparse
import blwz
import dx

def resolve(args):
    """argument action resolver"""
    return

def main(parser: argparse.ArgumentParser):
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
        description = HELP,
        epilog = 'Thanks.\nThe Management.')
    parser.add_argument('--version', action = 'version', version = '%(prog)s ' + VERSION)
    parser.set_defaults(func = resolve)
    main(parser)
    args = parser.parse_args()
    args.func(args)
