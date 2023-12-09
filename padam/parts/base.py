from __future__ import annotations
import collections
from typing import Any, Dict, List, Optional, OrderedDict
from solid import OpenSCADObject


class Part:
    def __init__(self, name: Optional[str] = None, settings: Optional[Dict[str, Any]] = dict()):
        self.name = name
        self.settings = settings
        self._parts = []

    def __str__(self):
        return self.name or super().__str__()

    def add_part(self, part: Part) -> Part:
        part.settings = self.settings
        self._parts.append(part)
        return part

    @property
    def parts(self):
        return self._parts

    @property
    def materials(self):
        names = []
        if self.name:
            names.append(self.name)
        if self.parts:
            materials = []
            for part in self.parts:
                for material in part.materials:
                    material['names'] = names + material['names']
                    materials.append(material)
            return materials
        else:
            return [dict(names=names, part=self)]

    def get_object(self) -> OpenSCADObject:
        raise NotImplementedError()

    def get_objects(self) -> List[OpenSCADObject]:
        return [self.get_object()]

    def get_params(self) -> OrderedDict[str, Any]:
        return collections.OrderedDict([('name', self.name or '')])

    def run(self, **kwargs):
        from padam.command import run
        run(self, **kwargs)
