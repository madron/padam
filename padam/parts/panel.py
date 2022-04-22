from typing import Optional
from padam.parts import Part


class Panel(Part):
    def __init__(
        self,
        length: float,
        width: float,
        thickness: float,
        material: Optional[str] = None,
    ):
        super().__init__()
        self.length = length
        self.width = width
        self.thickness = thickness
        self.material = material

    def get_object(self):
        import cadquery as cq
        return cq.Workplane().box(self.length, self.width, self.thickness)
