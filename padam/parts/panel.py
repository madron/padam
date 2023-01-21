from typing import List, Optional
from solid import (
    cube,
    OpenSCADObject,
)
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
        return self.bom_part(obj, 'panel', length=self.length, width=self.width, thickness=self.thickness)
