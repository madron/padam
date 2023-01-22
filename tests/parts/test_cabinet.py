import unittest
from padam.parts.cabinet import Cabinet


class CabinetTest(unittest.TestCase):
    def test_str(self):
        cabinet = Cabinet(name='kitchen')
        self.assertEqual(str(cabinet), 'kitchen')

    def test_parts_no_doors(self):
        cabinet = Cabinet(1000, 30, 18)
        self.assertEqual(len(cabinet.parts), 5)
        self.assertEqual(cabinet.parts[0].name, 'top_panel')
        self.assertEqual(cabinet.parts[1].name, 'bottom_panel')
        self.assertEqual(cabinet.parts[2].name, 'left_panel')
        self.assertEqual(cabinet.parts[3].name, 'right_panel')
        self.assertEqual(cabinet.parts[4].name, 'back_panel')

    def test_parts_1_door(self):
        cabinet = Cabinet(1000, 30, 18, door_number=1)
        self.assertEqual(len(cabinet.parts), 6)
        self.assertEqual(cabinet.parts[0].name, 'top_panel')
        self.assertEqual(cabinet.parts[1].name, 'bottom_panel')
        self.assertEqual(cabinet.parts[2].name, 'left_panel')
        self.assertEqual(cabinet.parts[3].name, 'right_panel')
        self.assertEqual(cabinet.parts[4].name, 'back_panel')
        self.assertEqual(cabinet.parts[5].name, 'door_panel')

    def test_parts_2_doors(self):
        cabinet = Cabinet(1000, 30, 18, door_number=2)
        self.assertEqual(len(cabinet.parts), 7)
        self.assertEqual(cabinet.parts[0].name, 'top_panel')
        self.assertEqual(cabinet.parts[1].name, 'bottom_panel')
        self.assertEqual(cabinet.parts[2].name, 'left_panel')
        self.assertEqual(cabinet.parts[3].name, 'right_panel')
        self.assertEqual(cabinet.parts[4].name, 'back_panel')
        self.assertEqual(cabinet.parts[5].name, 'left_door_panel')
        self.assertEqual(cabinet.parts[6].name, 'right_door_panel')

    def test_materials(self):
        cabinet = Cabinet(1000, 30, 18)
        self.assertEqual(len(cabinet.materials), 5)
        self.assertEqual(cabinet.materials[0].name, 'top_panel')
        self.assertEqual(cabinet.materials[1].name, 'bottom_panel')
        self.assertEqual(cabinet.materials[2].name, 'left_panel')
        self.assertEqual(cabinet.materials[3].name, 'right_panel')
        self.assertEqual(cabinet.materials[4].name, 'back_panel')

    def test_materials_1_door(self):
        cabinet = Cabinet(1000, 30, 18, door_number=1)
        self.assertEqual(len(cabinet.materials), 6)
        self.assertEqual(cabinet.materials[0].name, 'top_panel')
        self.assertEqual(cabinet.materials[1].name, 'bottom_panel')
        self.assertEqual(cabinet.materials[2].name, 'left_panel')
        self.assertEqual(cabinet.materials[3].name, 'right_panel')
        self.assertEqual(cabinet.materials[4].name, 'back_panel')
        self.assertEqual(cabinet.materials[5].name, 'door_panel')

    def test_materials_2_doors(self):
        cabinet = Cabinet(1000, 30, 18, door_number=2)
        self.assertEqual(len(cabinet.materials), 7)
        self.assertEqual(cabinet.materials[0].name, 'top_panel')
        self.assertEqual(cabinet.materials[1].name, 'bottom_panel')
        self.assertEqual(cabinet.materials[2].name, 'left_panel')
        self.assertEqual(cabinet.materials[3].name, 'right_panel')
        self.assertEqual(cabinet.materials[4].name, 'back_panel')
        self.assertEqual(cabinet.materials[5].name, 'left_door_panel')
        self.assertEqual(cabinet.materials[6].name, 'right_door_panel')

    def test_get_objects_no_doors(self):
        objs = Cabinet(name='kitchen', length=1200, depth=600, thickness=20).get_objects()
        self.assertEqual(len(objs), 5)

    def test_get_objects_1_door(self):
        objs = Cabinet(name='kitchen', length=1200, depth=600, thickness=20, door_number=1).get_objects()
        self.assertEqual(len(objs), 6)

    def test_get_objects_2_doors(self):
        objs = Cabinet(name='kitchen', length=1200, depth=600, thickness=20, door_number=2).get_objects()
        self.assertEqual(len(objs), 7)
