from typing import List, Optional
from padam.parts.panel import Panel
from padam.parts.frame import Frame
from solid import OpenSCADObject, rotate
from solid.utils import back, right, up


class Cabinet(Frame):
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
        back_thickness: Optional[float] = None,
        back_material: Optional[str] = None,
        door_number: Optional[int] = 0,
        door_thickness: Optional[float] = None,
        door_material: Optional[str] = None,
        door_offset: Optional[float] = 3,
        name: Optional[str] = None,
    ):
        super().__init__(
            length=length,
            height=height,
            depth=depth,
            thickness=thickness,
            material=material,
            top_thickness=top_thickness,
            bottom_thickness=bottom_thickness,
            side_thickness=side_thickness,
            top_material=top_material,
            bottom_material=bottom_material,
            side_material=side_material,
            name=name,
        )
        self.back_thickness = back_thickness or thickness
        self.back_material = back_material or material
        self.door_thickness = door_thickness or thickness
        self.door_material = door_material or material
        self.door_number = door_number
        self.door_offset = door_offset
        # calculated attributes
        self.interior_depth: float = self.depth - self.back_thickness
        # parts
        self.back_panel = self.add_part(Panel(self.interior_length, self.interior_height, self.back_thickness, name='back_panel', material=self.back_material))
        if self.door_number == 1:
            self.door_panel = self.add_part(Panel(self.height - self.door_offset, self.length - self.door_offset, self.door_thickness, name='door_panel', material=self.door_material))
        if self.door_number == 2:
            self.left_door_panel = self.add_part(Panel(self.height - self.door_offset, self.length / 2 - self.door_offset, self.door_thickness, name='left_door_panel', material=self.door_material))
            self.right_door_panel = self.add_part(Panel(self.height - self.door_offset, self.length / 2 - self.door_offset, self.door_thickness, name='right_door_panel', material=self.door_material))

    def get_objects(self) -> List[OpenSCADObject]:
        back_panel = right(self.side_thickness)(up(self.bottom_thickness)(rotate([90, 0, 0])(self.back_panel.get_object())))
        doors = []
        if self.door_number == 1:
            door = rotate([270, 270, 0])(self.door_panel.get_object())
            door = right(self.door_offset / 2)(door)
            doors.append(door)
        if self.door_number == 2:
            door = rotate([270, 270, 0])(self.left_door_panel.get_object())
            door = right(self.door_offset / 2)(door)
            doors.append(door)
            door = rotate([270, 270, 0])(self.right_door_panel.get_object())
            door = right(self.length / 2 + self.door_offset / 2)(door)
            doors.append(door)
        doors = [back(self.depth + self.door_thickness + 1)(door) for door in doors]
        doors = [up(self.door_offset / 2)(door) for door in doors]
        return super().get_objects() + [back_panel] + doors

    def get_params(self) -> List[tuple]:
        return super().get_params() + [
            ('back_thickness', self.back_thickness),
            ('back_material', self.back_material),
            ('door_number', self.door_number),
            ('door_thickness', self.door_thickness),
            ('door_material', self.door_material),
            ('door_offset', self.door_offset),
        ]
