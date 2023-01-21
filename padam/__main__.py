import argparse
from importlib import import_module
from pathlib import Path
from solid import scad_render


def get_projects():
    path = Path(__file__).parent / Path('projects')
    return [p.stem for p in path.iterdir()]


parser = argparse.ArgumentParser(
    prog = 'Padam',
    description = 'Python Aided Design And Manifacturing',
)
parser.add_argument('project', type=str, choices=get_projects())
parser.add_argument('file', type=argparse.FileType('w'))
args = parser.parse_args()


project = import_module('padam.projects.{}'.format(args.project))
rendered = ''.join([scad_render(obj) for obj in project.part.get_objects()])
args.file.write(rendered)
args.file.close()