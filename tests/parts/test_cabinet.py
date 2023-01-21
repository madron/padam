import unittest
from solid import cube, OpenSCADObject
from padam.parts.cabinet import Cabinet


class CabinetTest(unittest.TestCase):
    def test_str(self):
        cabinet = Cabinet(name='kitchen')
        self.assertEqual(str(cabinet), 'kitchen')

    def test_parts(self):
        cabinet = Cabinet(1000, 30, 18)
        self.assertEqual(len(cabinet.parts), 4)
        self.assertEqual(cabinet.parts[0].name, 'top_panel')
        self.assertEqual(cabinet.parts[1].name, 'bottom_panel')
        self.assertEqual(cabinet.parts[2].name, 'left_panel')
        self.assertEqual(cabinet.parts[3].name, 'right_panel')

    def test_materials(self):
        cabinet = Cabinet(1000, 30, 18)
        self.assertEqual(len(cabinet.materials), 4)
        self.assertEqual(cabinet.materials[0].name, 'top_panel')
        self.assertEqual(cabinet.materials[1].name, 'bottom_panel')
        self.assertEqual(cabinet.materials[2].name, 'left_panel')
        self.assertEqual(cabinet.materials[3].name, 'right_panel')

    def test_get_objects(self):
        objs = Cabinet(name='kitchen', length=1200, depth=600, thickness=20).get_objects()
        self.assertEqual(len(objs), 4)
