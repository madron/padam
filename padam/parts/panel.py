from typing import Any, List, Optional, OrderedDict
from solid import (
    color,
    cube,
    OpenSCADObject,
)
from padam import constants
from padam.parts import Part


class Panel(Part):
    def __init__(
        self,
        length: float,
        width: float,
        thickness: float,
        material: Optional[str] = None,
        name: Optional[str] = None,
    ):
        super().__init__(name=name)
        self.length = length
        self.width = width
        self.thickness = thickness
        self.material = material

    def get_object(self) -> OpenSCADObject:
        obj = cube([self.length, self.width, self.thickness])
        material_color = constants.MATERIAL_COLOR.get(self.material, None)
        if material_color:
            obj = color(material_color)(obj)
        return self.bom_part(obj, 'panel', length=self.length, width=self.width, thickness=self.thickness)

    def get_params(self) -> OrderedDict[str, Any]:
        params = super().get_params()
        params['material'] = self.material or ''
        params['length'] = self.length
        params['width'] = self.width
        params['thickness'] = self.thickness
        return params
