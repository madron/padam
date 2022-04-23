from typing import Optional
from padam.parts import Part
from padam.parts.panel import Panel


class Cabinet(Part):
    def __init__(
        self,
        length: Optional[int] = 1200,
        height: Optional[int] = 700,
        depth: Optional[int] = 600,
        thickness: Optional[float] = 18,
        top_thickness: Optional[float] = None,
        bottom_thickness: Optional[float] = None,
        side_thickness: Optional[float] = None,
        top_slitted: Optional[bool] = True,
        top_front_depth: Optional[int] = 100,
        top_back_depth: Optional[int] = 100,
        name: Optional[str] = None,
    ):
        super().__init__(name=name)
        self.length = length
        self.height = height
        self.depth = depth
        self.top_thickness = top_thickness or thickness
        self.bottom_thickness = bottom_thickness or thickness
        self.side_thickness = side_thickness or thickness
        self.top_slitted = top_slitted
        self.top_front_depth = top_front_depth
        self.top_back_depth = top_back_depth
        # calculated attributes
        self.interior_length: float = self.length - 2 * self.side_thickness
        # parts
        self.top_panel = self.add_part(Panel(self.interior_length, self.depth, self.top_thickness, name='top_panel'))
        self.bottom_panel = self.add_part(Panel(self.interior_length, self.depth, self.bottom_thickness, name='bottom_panel'))
        self.left_panel = self.add_part(Panel(self.height, self.depth, self.side_thickness, name='left_panel'))
        self.right_panel = self.add_part(Panel(self.height, self.depth, self.side_thickness, name='right_panel'))

    def get_object(self):
        import cadquery as cq
        a = cq.Assembly()
        # bottom
        a.add(
            self.bottom_panel,
            name=str(self.bottom_panel),
            loc=cq.Location(cq.Vector(self.interior_length / 2 + self.side_thickness, self.depth / 2, self.bottom_thickness / 2)),
            color=cq.Color('burlywood'),
        )
        # # left
        # a.add(
        #     self.left_panel,
        #     name=str(self.left_panel),
        #     loc=cq.Location(cq.Vector(self.side_thickness / 2, self.depth / 2, self.height / 2)),
        #     color=cq.Color('burlywood'),
        # )
        # right
        # a.add(
        #     self.right_panel,
        #     name=str(self.right_panel),
        #     loc=cq.Location(cq.Vector(- self.side_thickness / 2 + self.length, self.depth / 2, self.height / 2)),
        #     color=cq.Color('burlywood'),
        # )
        return a
