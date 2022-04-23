from typing import Optional
from padam.freecad import document
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

    def get_object(self, document=document):
        obj = document.addObject("Part::Box","Box")
        obj.Length = self.length
        obj.Width = self.width
        obj.Height = self.thickness
        if self.name:
            obj.Label = self.name
        return obj
