from typing import Any, List, Optional, OrderedDict
from padam.parts import Part
from padam.parts.panel import Panel
from solid import OpenSCADObject, rotate
from solid.utils import back, right, up


class Frame(Part):
    def __init__(
        self,
        length: Optional[int] = 1200,
        height: Optional[int] = 700,
        depth: Optional[int] = 600,
        thickness: Optional[float] = 18,
        material: Optional[str] = None,
        top_thickness: Optional[float] = None,
        bottom_thickness: Optional[float] = None,
        side_thickness: Optional[float] = None,
        top_material: Optional[str] = None,
        bottom_material: Optional[str] = None,
        side_material: Optional[str] = None,
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
        self.top_material = top_material or material
        self.bottom_material = bottom_material or material
        self.side_material = side_material or material
        self.top_slitted = top_slitted
        self.top_front_depth = top_front_depth
        self.top_back_depth = top_back_depth
        # calculated attributes
        self.interior_length: float = self.length - 2 * self.side_thickness
        self.interior_height: float = self.height - self.top_thickness - self.bottom_thickness
        # parts
        self.top_panel = self.add_part(Panel(self.interior_length, self.depth, self.top_thickness, name='top_panel', material=self.top_material))
        self.bottom_panel = self.add_part(Panel(self.interior_length, self.depth, self.bottom_thickness, name='bottom_panel', material=self.bottom_material))
        self.left_panel = self.add_part(Panel(self.height, self.depth, self.side_thickness, name='left_panel', material=self.side_material))
        self.right_panel = self.add_part(Panel(self.height, self.depth, self.side_thickness, name='right_panel', material=self.side_material))

    def get_objects(self) -> List[OpenSCADObject]:
        top_panel = up(self.height - self.top_thickness)(self.top_panel.get_object())
        bottom_panel = self.bottom_panel.get_object()
        left_panel = rotate([0, -90, 0])(self.left_panel.get_object())
        right_panel = right(self.length - self.side_thickness)(rotate([0, -90, 0])(self.right_panel.get_object()))
        panels = [top_panel, bottom_panel, left_panel, right_panel]
        panels = [right(self.side_thickness)(p) for p in panels]
        panels = [back(self.depth)(p) for p in panels]
        return panels

    def get_params(self) -> OrderedDict[str, Any]:
        params = super().get_params()
        params['length'] = self.length
        params['height'] = self.height
        params['depth'] = self.depth
        params['top_thickness'] = self.top_thickness
        params['bottom_thickness'] = self.bottom_thickness
        params['side_thickness'] = self.side_thickness
        params['top_material'] = self.top_material
        params['bottom_material'] = self.bottom_material
        params['side_material'] = self.side_material
        return params
