import argparse
import sys
from importlib import import_module
from pathlib import Path
from solid import scad_render
from padam.utils import get_cutlist


CUTLIST_FORMATS = ['cutlistoptimizer']


def get_projects():
    path = Path(__file__).parent / Path('projects')
    return [p.stem for p in path.iterdir()]


parser = argparse.ArgumentParser(
    prog = 'Padam',
    description = 'Python Aided Design And Manifacturing',
)
parser.add_argument('project', type=str, choices=get_projects())
parser.add_argument('-o', '--output', type=argparse.FileType('w'))
parser.add_argument('-q', '--quiet', action='store_true')
parser.add_argument('--cutlist', type=argparse.FileType('w'))
parser.add_argument('--cutlist-format', type=str, choices=CUTLIST_FORMATS, default=CUTLIST_FORMATS[0])
args = parser.parse_args()


project = import_module('padam.projects.{}'.format(args.project))

if not args.quiet:
    sys.stdout.write('Parameters\n')
    sys.stdout.write('----------\n')
    params = project.part.get_params()
    for param in params:
        if isinstance(param[1], str):
            line = '{}: {}\n'.format(*param)
        else:
            line = '{:20}: {}\n'.format(*param)
        sys.stdout.write(line)
    if params:
        sys.stdout.write('\n')

if args.output:
    rendered = ''.join([scad_render(obj) for obj in project.part.get_objects()])
    args.output.write(rendered)
    args.output.close()


if args.cutlist:
    args.cutlist.write(get_cutlist(project.part))
    args.cutlist.close()
