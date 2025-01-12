import sys
import yaml
from solid import scad_render
from padam import Project
from padam.constants import CUTLIST_DEFAULT_FORMAT
from padam.utils import get_cutlist


def run(project, output=None, quiet=False, cutlist=False, cutlist_format=CUTLIST_DEFAULT_FORMAT):
    project: Project = Project(**yaml.safe_load(project))

    if not quiet:
        sys.stdout.write('Parameters\n')
        sys.stdout.write('----------\n')
        sys.stdout.write('\n')
        for part in project.part.values():
            sys.stdout.write('{}\n'.format(part.name))
            sys.stdout.write('----------\n')
            params = part.get_params()
            for key, value in params.items():
                line = '{:20}: {}\n'.format(key, value)
                sys.stdout.write(line)
            if params:
                sys.stdout.write('\n')

    if output:
        rendered = ''.join([scad_render(obj) for obj in project.get_objects()])
        output.write(rendered)
        output.close()

    if cutlist:
        cutlist.write(get_cutlist(project, format=cutlist_format))
        cutlist.close()
