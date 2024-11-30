from typing import Any, List, OrderedDict
from padam.parts import Part
from padam.parts.panel import Panel
from solid import OpenSCADObject, rotate
from solid.utils import back, right, up


class Frame(Part):
    length: int | None = None
    height: int | None = None
    depth: int | None = None
    thickness: float | None = None
    material: str | None = None
    top_thickness: float | None = None
    bottom_thickness: float | None = None
    side_thickness: float | None = None
    top_material: str | None = None
    bottom_material: str | None = None
    side_material: str | None = None
    top_slitted: bool | None = True
    top_front_depth: int | None = 100
    top_back_depth: int | None = 100
    # calculated attributes
    interior_length: float | None = None
    interior_height: float | None = None
    # parts
    top_panel: Panel | None = None
    bottom_panel: Panel | None = None
    left_panel: Panel | None = None
    right_panel: Panel | None = None

    def __init__(
        self,
        length: float | None = None,
        height: float | None = None,
        depth: float | None = None,
        **kwargs,
    ):
        super().__init__(
            length=length or kwargs.get('length', None),
            height=height or kwargs.get('height', None),
            depth=depth or kwargs.get('depth', None),
            **kwargs,
        )

    def model_post_init(self, __context: Any) -> None:
        # defaults
        self.length = self.length or 1200
        self.height = self.height or 700
        self.depth = self.depth or 600
        self.thickness = self.thickness or 18
        self.top_thickness = self.top_thickness or self.thickness
        self.bottom_thickness = self.bottom_thickness or self.thickness
        self.side_thickness = self.side_thickness or self.thickness
        self.top_material = self.top_material or self.material
        self.bottom_material = self.bottom_material or self.material
        self.side_material = self.side_material or self.material
        # calculated attributes
        self.interior_length = self.length - 2 * self.side_thickness
        self.interior_height = self.height - self.top_thickness - self.bottom_thickness
        # parts
        p = Panel(self.interior_length, self.depth, self.top_thickness, name='top_panel', material=self.top_material)
        self.top_panel = self.add_part(p)
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
        panels = [self.translate_object(p) for p in panels]
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
