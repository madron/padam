from __future__ import annotations
from typing import List, Optional
from solid import OpenSCADObject


class Part:
    def __init__(self, name: Optional[str] = None):
        self.name = name
        self._parts = []

    def __str__(self):
        return self.name or super().__str__()

    def add_part(self, part: Part) -> Part:
        self._parts.append(part)
        return part

    @property
    def parts(self):
        return self._parts

    @property
    def materials(self):
        if self.parts:
            materials = []
            for part in self.parts:
                materials.extend(part.materials)
            return materials
        else:
            return [self]

    def get_object(self) -> OpenSCADObject:
        raise NotImplementedError()

    def get_objects(self) -> List[OpenSCADObject]:
        return [self.get_object()]
