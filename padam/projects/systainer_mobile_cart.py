from typing import List
from padam.parts import Container
from padam.parts.frame import Frame

THICKNESS = 20
TOP_THICKNESS = 28
BOTTOM_THICKNESS = 28
ROLLER_HEIGHT = 124 + 2.5

TOTAL_HEIGHT = 900
INTERNAL_COMPARTMENT_LENGHT = 420
DRAWER_SLIDER_LENGHT = 450

CABINET_LENGTH = 2 * INTERNAL_COMPARTMENT_LENGHT + 3 * THICKNESS
CABINET_HEIGHT = TOTAL_HEIGHT - ROLLER_HEIGHT - TOP_THICKNESS
CABINET_DEPTH = DRAWER_SLIDER_LENGHT


class Cart(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cabinet = self.add_part(
            Frame(
                name='cabinet',
                length=CABINET_LENGTH,
                height=CABINET_HEIGHT,
                depth=CABINET_DEPTH,
                thickness=THICKNESS,
                bottom_thickness=BOTTOM_THICKNESS,
                material='plywood',
            )
        )

    def get_params(self) -> List[tuple]:
        params = self.cabinet.get_params()
        params['name'] = self.name
        return params


part = Cart(name='cart')
