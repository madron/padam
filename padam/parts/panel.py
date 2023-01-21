from typing import List, Optional
from solid import (
    cube,
    OpenSCADObject,
)
from solid.utils import bom_part
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
        return cube([self.length, self.width, self.thickness])
