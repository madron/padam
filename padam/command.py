import argparse
import sys
from solid import scad_render
from padam.utils import get_cutlist


CUTLIST_FORMATS = ['cutlistoptimizer']


def run(part):
    parser = argparse.ArgumentParser(
        prog = 'Padam',
        description = 'Python Aided Design And Manifacturing',
    )
    parser.add_argument('-o', '--output', type=argparse.FileType('w'))
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('--cutlist', type=argparse.FileType('w'))
    parser.add_argument('--cutlist-format', type=str, choices=CUTLIST_FORMATS, default=CUTLIST_FORMATS[0])
    args = parser.parse_args()

    if not args.quiet:
        sys.stdout.write('Parameters\n')
        sys.stdout.write('----------\n')
        params = part.get_params()
        for key, value in params.items():
            line = '{:20}: {}\n'.format(key, value)
            sys.stdout.write(line)
        if params:
            sys.stdout.write('\n')

    if args.output:
        rendered = ''.join([scad_render(obj) for obj in part.get_objects()])
        args.output.write(rendered)
        args.output.close()


    if args.cutlist:
        args.cutlist.write(get_cutlist(part))
        args.cutlist.close()
