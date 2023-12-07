import unittest
from padam.parts.frame import Frame


class FrameTest(unittest.TestCase):
    def test_str(self):
        frame = Frame(name='kitchen')
        self.assertEqual(str(frame), 'kitchen')

    def test_parts(self):
        frame = Frame(1000, 30, 18)
        self.assertEqual(len(frame.parts), 4)
        self.assertEqual(frame.parts[0].name, 'top_panel')
        self.assertEqual(frame.parts[1].name, 'bottom_panel')
        self.assertEqual(frame.parts[2].name, 'left_panel')
        self.assertEqual(frame.parts[3].name, 'right_panel')

    def test_materials(self):
        frame = Frame(1000, 30, 18)
        self.assertEqual(len(frame.materials), 4)
        self.assertEqual(frame.materials[0].name, 'top_panel')
        self.assertEqual(frame.materials[1].name, 'bottom_panel')
        self.assertEqual(frame.materials[2].name, 'left_panel')
        self.assertEqual(frame.materials[3].name, 'right_panel')

    def test_get_objects(self):
        objs = Frame(name='kitchen', length=1200, height=700, depth=600, thickness=20).get_objects()
        self.assertEqual(len(objs), 4)

    def test_get_params(self):
        params = Frame(length=1200, height=700, depth=600, thickness=20, material='plywood').get_params()
        self.assertEqual(len(params), 10)
        self.assertEqual(params['name'], '')
        self.assertEqual(params['length'], 1200)
        self.assertEqual(params['height'], 700)
        self.assertEqual(params['depth'], 600)
        self.assertEqual(params['top_thickness'], 20)
        self.assertEqual(params['bottom_thickness'], 20)
        self.assertEqual(params['side_thickness'], 20)
        self.assertEqual(params['top_material'], 'plywood')
        self.assertEqual(params['bottom_material'], 'plywood')
        self.assertEqual(params['side_material'], 'plywood')
