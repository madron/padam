import argparse
from padam import constants
from padam.command import run


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog = 'padam',
        description = 'Python Aided Design And Manifacturing',
    )
    parser.add_argument('project', type=argparse.FileType('r'), help='Project file in yaml format')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), help='Openscad format')
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('--cutlist', type=argparse.FileType('w'))
    parser.add_argument('--cutlist-format', type=str, choices=constants.CUTLIST_FORMATS, default=constants.CUTLIST_DEFAULT_FORMAT)
    args = vars(parser.parse_args())
    run(**args)
