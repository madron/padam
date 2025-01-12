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

    def test_float(self):
        frame = Frame(1000.5, 800.5, 400.5)
        self.assertEqual(len(frame.parts), 4)
        self.assertEqual(frame.parts[0].name, 'top_panel')
        self.assertEqual(frame.parts[0].length, 964.5)
        self.assertEqual(frame.parts[0].width, 400.5)
        self.assertEqual(frame.parts[1].name, 'bottom_panel')
        self.assertEqual(frame.parts[1].length, 964.5)
        self.assertEqual(frame.parts[1].width, 400.5)
        self.assertEqual(frame.parts[2].name, 'left_panel')
        self.assertEqual(frame.parts[2].length, 800.5)
        self.assertEqual(frame.parts[3].width, 400.5)
        self.assertEqual(frame.parts[3].name, 'right_panel')
        self.assertEqual(frame.parts[3].length, 800.5)
        self.assertEqual(frame.parts[3].width, 400.5)

    def test_materials(self):
        frame = Frame(1000, 30, 18)
        self.assertEqual(len(frame.get_materials()), 4)
        self.assertEqual(frame.get_materials()[0]['part'].name, 'top_panel')
        self.assertEqual(frame.get_materials()[1]['part'].name, 'bottom_panel')
        self.assertEqual(frame.get_materials()[2]['part'].name, 'left_panel')
        self.assertEqual(frame.get_materials()[3]['part'].name, 'right_panel')

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
