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

    def test_default(self):
        cabinet = Cabinet(600, 400, default=dict(thickness=22))
        self.assertEqual(cabinet.thickness, 22)

    def test_materials(self):
        cabinet = Cabinet(1000, 30, 18)
        self.assertEqual(len(cabinet.materials), 5)
        self.assertEqual(cabinet.materials[0]['part'].name, 'top_panel')
        self.assertEqual(cabinet.materials[1]['part'].name, 'bottom_panel')
        self.assertEqual(cabinet.materials[2]['part'].name, 'left_panel')
        self.assertEqual(cabinet.materials[3]['part'].name, 'right_panel')
        self.assertEqual(cabinet.materials[4]['part'].name, 'back_panel')

    def test_materials_1_door(self):
        cabinet = Cabinet(1000, 30, 18, door_number=1)
        self.assertEqual(len(cabinet.materials), 6)
        self.assertEqual(cabinet.materials[0]['part'].name, 'top_panel')
        self.assertEqual(cabinet.materials[1]['part'].name, 'bottom_panel')
        self.assertEqual(cabinet.materials[2]['part'].name, 'left_panel')
        self.assertEqual(cabinet.materials[3]['part'].name, 'right_panel')
        self.assertEqual(cabinet.materials[4]['part'].name, 'back_panel')
        self.assertEqual(cabinet.materials[5]['part'].name, 'door_panel')

    def test_materials_2_doors(self):
        cabinet = Cabinet(1000, 30, 18, door_number=2)
        self.assertEqual(len(cabinet.materials), 7)
        self.assertEqual(cabinet.materials[0]['part'].name, 'top_panel')
        self.assertEqual(cabinet.materials[1]['part'].name, 'bottom_panel')
        self.assertEqual(cabinet.materials[2]['part'].name, 'left_panel')
        self.assertEqual(cabinet.materials[3]['part'].name, 'right_panel')
        self.assertEqual(cabinet.materials[4]['part'].name, 'back_panel')
        self.assertEqual(cabinet.materials[5]['part'].name, 'left_door_panel')
        self.assertEqual(cabinet.materials[6]['part'].name, 'right_door_panel')

    def test_get_objects_no_doors(self):
        objs = Cabinet(name='kitchen', length=1200, height=700, depth=600, thickness=20).get_objects()
        self.assertEqual(len(objs), 5)

    def test_get_objects_1_door(self):
        objs = Cabinet(name='kitchen', length=1200, height=700, depth=600, thickness=20, door_number=1).get_objects()
        self.assertEqual(len(objs), 6)

    def test_get_objects_2_doors(self):
        objs = Cabinet(name='kitchen', length=1200, height=700, depth=600, thickness=20, door_number=2).get_objects()
        self.assertEqual(len(objs), 7)

    def test_get_params(self):
        params = Cabinet(name='kitchen', length=1200, height=700, depth=600, thickness=20, door_number=2, material='plywood').get_params()
        self.assertEqual(len(params), 19)
        self.assertEqual(params['name'], 'kitchen')
        self.assertEqual(params['length'], 1200)
        self.assertEqual(params['height'], 700)
        self.assertEqual(params['depth'], 600)
        self.assertEqual(params['interior_length'], 1160)
        self.assertEqual(params['interior_height'], 660)
        self.assertEqual(params['interior_depth'], 580)
        self.assertEqual(params['top_thickness'], 20)
        self.assertEqual(params['bottom_thickness'], 20)
        self.assertEqual(params['side_thickness'], 20)
        self.assertEqual(params['top_material'], 'plywood')
        self.assertEqual(params['bottom_material'], 'plywood')
        self.assertEqual(params['side_material'], 'plywood')
        self.assertEqual(params['back_thickness'], 20)
        self.assertEqual(params['back_material'], 'plywood')
        self.assertEqual(params['reveal'], 2)
        self.assertEqual(params['door_number'], 2)
        self.assertEqual(params['door_thickness'], 20)
        self.assertEqual(params['door_material'], 'plywood')
