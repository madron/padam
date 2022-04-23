import os
import subprocess
import sys
from importlib import import_module
from pathlib import Path
from types import ModuleType


FREECAD_MODULES = [
    'FreeCAD',
    'Part',
]


def _add_freecad_to_sys_path():
    for path in _get_freecad_paths():
        sys.path.append(path)


def _get_freecad_paths():
    freecad_command = os.getenv('FREECAD_COMMAND', 'freecadcmd')
    script_path = Path(__file__).parent / '_get_paths.py'
    output = subprocess.check_output([freecad_command, script_path])
    paths = []
    for line in output.splitlines():
        if line == b'__end__':
            break
        path = line.decode('utf8')
        if Path(path).exists() and path not in sys.path:
            paths.append(path)
    return paths


try:
    _add_freecad_to_sys_path()
    for module in FREECAD_MODULES:
        globals()[module] = import_module(module)
    freecad_missing = False
    document = globals()['FreeCAD'].ActiveDocument or globals()['FreeCAD'].newDocument()
except:
    raise
    freecad_missing = True
    for module in FREECAD_MODULES:
        globals()[module] = ModuleType('FreeCADFake')
    document = None


if __name__ == '__main__':
    print(_get_freecad_paths())
