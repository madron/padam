from __future__ import annotations
from itertools import zip_longest
from typing import List, Optional
from solid import OpenSCADObject
from solid.utils import g_bom_headers


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

    def bom_part(self, obj: OpenSCADObject, description: str='', per_unit_price:float=None, currency: str='US$', *args, **kwargs) -> OpenSCADObject:
        name = description if description else obj.__name__

        elements = {'name': name, 'Count':0, 'currency':currency, 'Unit Price':per_unit_price}
        # This update also adds empty key value pairs to prevent key exceptions.
        elements.update(dict(zip_longest(g_bom_headers, args, fillvalue='')))
        elements.update(kwargs)

        obj.add_trait('BOM', elements)
        return obj
