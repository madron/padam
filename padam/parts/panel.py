from typing import Any, Dict, List, OrderedDict
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
    length: float
    width: float
    thickness: float
    material: str | None = None
    cut_length_oversize: float | None = 0
    cut_width_oversize: float | None = 0
    cut_thickness_oversize: float | None = 0

    def __init__(
        self,
        length: float | None = None,
        width: float | None = None,
        thickness: float | None = None,
        **kwargs,
    ):
      super().__init__(
          length=length or kwargs.get('length', None),
          width=width or kwargs.get('width', None),
          thickness=thickness or kwargs.get('thickness', None),
          **kwargs,
        )

    def model_post_init(self, __context: Any) -> None:
        # defaults
        self.material = self.material or ''

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

    def get_panel_cut(self) -> Dict[str, Any]:
        return dict(
            length=self.length + self.cut_length_oversize,
            width=self.width + self.cut_width_oversize,
            thickness=self.thickness + self.cut_thickness_oversize,
            material=self.material or ''
        )


class EdgeBandedPanel(Panel):
    front_edge_banding_thickness: float | None = None,
    back_edge_banding_thickness: float | None = None,
    left_edge_banding_thickness: float | None = None,
    right_edge_banding_thickness: float | None = None,
    edge_banding_material: str | None = 'hardwood',
    edge_banding_style: str | None = 'length',

    def model_post_init(self, __context: Any) -> None:
        self._edge_band_cut_length_oversize = self.cut_length_oversize or 0
        self._edge_band_cut_width_oversize = self.cut_width_oversize or 0
        self._edge_band_cut_thickness_oversize = self.cut_thickness_oversize or 0
        # calculated
        self._main_panel_length = self.length
        self._main_panel_width = self.width
        if self.front_edge_banding_thickness:
            self._main_panel_width -= self.front_edge_banding_thickness
            if self.edge_banding_style in ['overlap', 'length']:
                length = self.length
            elif self.edge_banding_style == 'width':
                length = self.length - (self.left_edge_banding_thickness or 0) - (self.right_edge_banding_thickness or 0)
            self._front_edge = self.add_part(Panel(
                name='front_edge',
                length=length,
                width=self.front_edge_banding_thickness,
                thickness=self.thickness,
                material=self.edge_banding_material,
                cut_length_oversize=self._edge_band_cut_length_oversize,
                cut_width_oversize=self._edge_band_cut_width_oversize,
                cut_thickness_oversize=self._edge_band_cut_thickness_oversize,
            ))
        if self.back_edge_banding_thickness:
            self._main_panel_width -= self.back_edge_banding_thickness
            if self.edge_banding_style in ['overlap', 'length']:
                length = self.length
            elif self.edge_banding_style == 'width':
                length = self.length - (self.left_edge_banding_thickness or 0) - (self.right_edge_banding_thickness or 0)
            self._back_edge = self.add_part(Panel(
                name='back_edge',
                length=length,
                width=self.back_edge_banding_thickness,
                thickness=self.thickness,
                material=self.edge_banding_material,
                cut_length_oversize=self._edge_band_cut_length_oversize,
                cut_width_oversize=self._edge_band_cut_width_oversize,
                cut_thickness_oversize=self._edge_band_cut_thickness_oversize,
            ))
        if self.left_edge_banding_thickness:
            self._main_panel_length -= self.left_edge_banding_thickness
            if self.edge_banding_style in ['overlap', 'width']:
                length = self.width
            elif self.edge_banding_style == 'length':
                length = self.width - (self.front_edge_banding_thickness or 0) - (self.back_edge_banding_thickness or 0)
            self._left_edge = self.add_part(Panel(
                name='left_edge',
                length=length,
                width=self.left_edge_banding_thickness,
                thickness=self.thickness,
                material=self.edge_banding_material,
                cut_length_oversize=self._edge_band_cut_length_oversize,
                cut_width_oversize=self._edge_band_cut_width_oversize,
                cut_thickness_oversize=self._edge_band_cut_thickness_oversize,
            ))
        if self.right_edge_banding_thickness:
            self._main_panel_length -= self.right_edge_banding_thickness
            if self.edge_banding_style in ['overlap', 'width']:
                length = self.width
            elif self.edge_banding_style == 'length':
                length = self.width - (self.front_edge_banding_thickness or 0) - (self.back_edge_banding_thickness or 0)
            self._right_edge = self.add_part(Panel(
                name='right_edge',
                length=length,
                width=self.right_edge_banding_thickness,
                thickness=self.thickness,
                material=self.edge_banding_material,
                cut_length_oversize=self._edge_band_cut_length_oversize,
                cut_width_oversize=self._edge_band_cut_width_oversize,
                cut_thickness_oversize=self._edge_band_cut_thickness_oversize,
            ))
        self._main_panel = self.add_part(Panel(
            length=self._main_panel_length,
            width=self._main_panel_width,
            thickness=self.thickness,
            material=self.material,
        ))

    def get_objects(self) -> List[OpenSCADObject]:
        main_panel = self._main_panel.get_object()
        objects = []
        if self.front_edge_banding_thickness:
            main_panel = forward(self.front_edge_banding_thickness)(main_panel)
            if self.edge_banding_style == 'width':
                offset = self.left_edge_banding_thickness or 0
                objects.append(right(offset)(self._front_edge.get_object()))
            else:
                objects.append(self._front_edge.get_object())
        if self.back_edge_banding_thickness:
            offset = (self.front_edge_banding_thickness or 0) + self._main_panel_width
            back_edge = forward(offset)(self._back_edge.get_object())
            if self.edge_banding_style == 'width':
                offset = self.left_edge_banding_thickness or 0
                objects.append(right(offset)(back_edge))
            else:
                objects.append(back_edge)
        if self.left_edge_banding_thickness:
            main_panel = right(self.left_edge_banding_thickness)(main_panel)
            left_edge = right(self.left_edge_banding_thickness)(rotate([0, 0, 90])(self._left_edge.get_object()))
            if self.edge_banding_style == 'length':
                offset = self.front_edge_banding_thickness or 0
                objects.append(forward(offset)(left_edge))
            else:
                objects.append(left_edge)
        if self.right_edge_banding_thickness:
            offset = (self.left_edge_banding_thickness or 0) + (self.right_edge_banding_thickness or 0) + self._main_panel_length
            right_edge = right(offset)(rotate([0, 0, 90])(self._right_edge.get_object()))
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
