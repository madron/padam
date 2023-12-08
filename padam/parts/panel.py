from typing import Any, List, Optional, OrderedDict
from solid import (
    color,
    cube,
    OpenSCADObject,
    rotate,
)
from solid.utils import forward, right
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
        return obj

    def get_params(self) -> OrderedDict[str, Any]:
        params = super().get_params()
        params['material'] = self.material or ''
        params['length'] = self.length
        params['width'] = self.width
        params['thickness'] = self.thickness
        return params


class EdgeBandedPanel(Part):
    def __init__(
        self,
        length: float,
        width: float,
        thickness: float,
        material: Optional[str] = None,
        name: Optional[str] = None,
        front_edge_banding_thickness: Optional[float] = None,
        back_edge_banding_thickness: Optional[float] = None,
        left_edge_banding_thickness: Optional[float] = None,
        right_edge_banding_thickness: Optional[float] = None,
        edge_banding_material: Optional[float] = 'hardwood',
        edge_banding_style: Optional[str] = 'length',
    ):
        super().__init__(name=name)
        self.length = length
        self.width = width
        self.thickness = thickness
        self.material = material
        self.front_edge_banding_thickness = front_edge_banding_thickness
        self.back_edge_banding_thickness = back_edge_banding_thickness
        self.left_edge_banding_thickness = left_edge_banding_thickness
        self.right_edge_banding_thickness = right_edge_banding_thickness
        self.edge_banding_material = edge_banding_material
        self.edge_banding_style = edge_banding_style
        # calculated
        self.main_panel_length = self.length
        self.main_panel_width = self.width
        if self.front_edge_banding_thickness:
            self.main_panel_width -= self.front_edge_banding_thickness
            if self.edge_banding_style in ['overlap', 'length']:
                length = self.length
            elif self.edge_banding_style == 'width':
                length = self.length - (self.left_edge_banding_thickness or 0) - (self.right_edge_banding_thickness or 0)
            self.front_edge = self.add_part(Panel(name='front_edge', length=length, width=self.front_edge_banding_thickness, thickness=self.thickness, material=self.edge_banding_material))
        if self.back_edge_banding_thickness:
            self.main_panel_width -= self.back_edge_banding_thickness
            if self.edge_banding_style in ['overlap', 'length']:
                length = self.length
            elif self.edge_banding_style == 'width':
                length = self.length - (self.left_edge_banding_thickness or 0) - (self.right_edge_banding_thickness or 0)
            self.back_edge = self.add_part(Panel(name='back_edge', length=length, width=self.back_edge_banding_thickness, thickness=self.thickness, material=self.edge_banding_material))
        if self.left_edge_banding_thickness:
            self.main_panel_length -= self.left_edge_banding_thickness
            if self.edge_banding_style in ['overlap', 'width']:
                length = self.width
            elif self.edge_banding_style == 'length':
                length = self.width - (self.front_edge_banding_thickness or 0) - (self.back_edge_banding_thickness or 0)
            self.left_edge = self.add_part(Panel(name='left_edge', length=length, width=self.left_edge_banding_thickness, thickness=self.thickness, material=self.edge_banding_material))
        if self.right_edge_banding_thickness:
            self.main_panel_length -= self.right_edge_banding_thickness
            if self.edge_banding_style in ['overlap', 'width']:
                length = self.width
            elif self.edge_banding_style == 'length':
                length = self.width - (self.front_edge_banding_thickness or 0) - (self.back_edge_banding_thickness or 0)
            self.right_edge = self.add_part(Panel(name='right_edge', length=length, width=self.right_edge_banding_thickness, thickness=self.thickness, material=self.edge_banding_material))
        self.main_panel = self.add_part(Panel(length=self.main_panel_length, width=self.main_panel_width, thickness=self.thickness, material=self.material))

    def get_objects(self) -> List[OpenSCADObject]:
        main_panel = self.main_panel.get_object()
        objects = []
        if self.front_edge_banding_thickness:
            main_panel = forward(self.front_edge_banding_thickness)(main_panel)
            if self.edge_banding_style == 'width':
                offset = self.left_edge_banding_thickness or 0
                objects.append(right(offset)(self.front_edge.get_object()))
            else:
                objects.append(self.front_edge.get_object())
        if self.back_edge_banding_thickness:
            offset = (self.front_edge_banding_thickness or 0) + self.main_panel_width
            back_edge = forward(offset)(self.back_edge.get_object())
            if self.edge_banding_style == 'width':
                offset = self.left_edge_banding_thickness or 0
                objects.append(right(offset)(back_edge))
            else:
                objects.append(back_edge)
        if self.left_edge_banding_thickness:
            main_panel = right(self.left_edge_banding_thickness)(main_panel)
            left_edge = right(self.left_edge_banding_thickness)(rotate([0, 0, 90])(self.left_edge.get_object()))
            if self.edge_banding_style == 'length':
                offset = self.front_edge_banding_thickness or 0
                objects.append(forward(offset)(left_edge))
            else:
                objects.append(left_edge)
        if self.right_edge_banding_thickness:
            offset = (self.left_edge_banding_thickness or 0) + (self.right_edge_banding_thickness or 0) + self.main_panel_length
            right_edge = right(offset)(rotate([0, 0, 90])(self.right_edge.get_object()))
            if self.edge_banding_style == 'length':
                offset = self.front_edge_banding_thickness or 0
                objects.append(forward(offset)(right_edge))
            else:
                objects.append(right_edge)
        objects.append(main_panel)
        return objects

    def get_params(self) -> OrderedDict[str, Any]:
        params = super().get_params()
        params['material'] = self.material or ''
        params['length'] = self.length
        params['width'] = self.width
        params['thickness'] = self.thickness
        return params
