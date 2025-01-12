from typing import Any, List, OrderedDict
from padam.parts.panel import BasePanel
from padam.parts.frame import Frame
from solid import OpenSCADObject, rotate
from solid.utils import back, right, up


class Cabinet(Frame):
    back_thickness: float | None = None
    back_material: str | None = None
    reveal: float | None = None
    door_number: int | None = None
    door_thickness: float | None = None
    door_material: str | None = None
    # calculated attributes
    interior_depth: float | None = None
    # parts
    back_panel: BasePanel | None = None
    door_panel: BasePanel | None = None
    left_door_panel: BasePanel | None = None
    right_door_panel: BasePanel | None = None

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        # defaults
        self.back_thickness = self.back_thickness or self.thickness
        self.back_material = self.back_material or self.material
        self.door_thickness = self.door_thickness or self.thickness
        self.door_material = self.door_material or self.material
        self.door_number = self.door_number or 0
        self.reveal = self.reveal or 2
        # calculated attributes
        door_offset = self.reveal * 2
        self.interior_depth: float = self.depth - self.back_thickness
        # parts
        self.back_panel = self.add_part(BasePanel(self.interior_length, self.interior_height, self.back_thickness, name='back_panel', material=self.back_material))
        if self.door_number == 1:
            self.door_panel = self.add_part(BasePanel(self.height - door_offset, self.length - door_offset, self.door_thickness, name='door_panel', material=self.door_material))
        if self.door_number == 2:
            self.left_door_panel = self.add_part(BasePanel(self.height - door_offset, self.length / 2 - door_offset, self.door_thickness, name='left_door_panel', material=self.door_material))
            self.right_door_panel = self.add_part(BasePanel(self.height - door_offset, self.length / 2 - door_offset, self.door_thickness, name='right_door_panel', material=self.door_material))

    def get_objects(self) -> List[OpenSCADObject]:
        door_offset = self.reveal * 2
        back_panel = right(self.side_thickness)(up(self.bottom_thickness)(rotate([90, 0, 0])(self.back_panel.get_object())))
        doors = []
        if self.door_number == 1:
            door = rotate([270, 270, 0])(self.door_panel.get_object())
            door = right(door_offset / 2)(door)
            doors.append(door)
        if self.door_number == 2:
            door = rotate([270, 270, 0])(self.left_door_panel.get_object())
            door = right(door_offset / 2)(door)
            doors.append(door)
            door = rotate([270, 270, 0])(self.right_door_panel.get_object())
            door = right(self.length / 2 + door_offset / 2)(door)
            doors.append(door)
        doors = [back(self.depth + self.door_thickness + 1)(door) for door in doors]
        doors = [up(door_offset / 2)(door) for door in doors]
        return super().get_objects() + [self.translate_object(self.rotate_object(back_panel))] + [self.translate_object(self.rotate_object(x)) for x in doors]

    def get_params(self) -> OrderedDict[str, Any]:
        params = super().get_params()
        params['back_thickness'] = self.back_thickness
        params['back_material'] = self.back_material
        params['interior_length'] = self.interior_length
        params['interior_height'] = self.interior_height
        params['interior_depth'] = self.interior_depth
        params['door_number'] = self.door_number
        if self.door_number:
            params['door_thickness'] = self.door_thickness
            params['door_material'] = self.door_material
            params['reveal'] = self.reveal
        return params
