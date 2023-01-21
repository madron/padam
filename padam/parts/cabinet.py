from typing import List, Optional
from padam.parts.panel import Panel
from padam.parts.frame import Frame
from solid import OpenSCADObject, rotate
from solid.utils import right, up, back


class Cabinet(Frame):
    def __init__(
        self,
        length: Optional[int] = 1200,
        height: Optional[int] = 700,
        depth: Optional[int] = 600,
        thickness: Optional[float] = 18,
        top_thickness: Optional[float] = None,
        bottom_thickness: Optional[float] = None,
        side_thickness: Optional[float] = None,
        back_thickness: Optional[float] = None,
        name: Optional[str] = None,
    ):
        super().__init__(
            length=length,
            height=height,
            depth=depth,
            thickness=thickness,
            top_thickness=top_thickness,
            bottom_thickness=bottom_thickness,
            side_thickness=side_thickness,
            name=name,
        )
        self.back_thickness = back_thickness or thickness
        # calculated attributes
        self.interior_depth: float = self.depth - self.back_thickness
        # parts
        self.back_panel = self.add_part(Panel(self.interior_length, self.interior_height, self.back_thickness, name='back_panel'))

    def get_objects(self) -> List[OpenSCADObject]:
        back_panel = right(self.side_thickness)(up(self.bottom_thickness)(rotate([90, 0, 0])(self.back_panel.get_object())))
        return super().get_objects() + [back_panel]
