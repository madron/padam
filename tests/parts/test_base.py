import collections
import unittest
from padam.parts import Part


class PartTest(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Part(name='mypart')), 'mypart')

    def test_default(self):
        default = dict(name='default-name')
        self.assertEqual(str(Part(default=default)), 'default-name')

    def test_no_parts(self):
        part = Part()
        self.assertEqual(part.parts, [])
        self.assertEqual(part.get_materials(), [dict(names=[], part=part)])

    def test_parts(self):
        panel = Part(name='panel')
        screw_1 = panel.add_part(Part(name='screw 1'))
        screw_2 = panel.add_part(Part(name='screw 2'))
        self.assertEqual(screw_1.name, 'screw 1')
        self.assertEqual(screw_2.name, 'screw 2')
        # parts
        self.assertEqual(panel.parts[0].name, 'screw 1')
        self.assertEqual(panel.parts[1].name, 'screw 2')
        self.assertEqual(len(panel.parts), 2)
        # materials
        self.assertEqual(panel.get_materials()[0]['part'].name, 'screw 1')
        self.assertEqual(panel.get_materials()[1]['part'].name, 'screw 2')
        self.assertEqual(len(panel.get_materials()), 2)

    def test_sub_parts(self):
        # drawer
        drawer = Part(name='drawer')
        drawer.add_part(Part(name='drawer_screw'))
        drawer.add_part(Part(name='drawer_panel'))
        # cabinet
        cabinet = Part(name='cabinet')
        cabinet.add_part(Part(name='cabinet_top'))
        cabinet.add_part(Part(name='cabinet_bottom'))
        cabinet.add_part(drawer)
        # parts
        self.assertEqual(cabinet.parts[0].name, 'cabinet_top')
        self.assertEqual(cabinet.parts[1].name, 'cabinet_bottom')
        self.assertEqual(cabinet.parts[2].name, 'drawer')
        self.assertEqual(len(cabinet.parts), 3)
        # materials
        self.assertEqual(cabinet.get_materials()[0]['part'].name, 'cabinet_top')
        self.assertEqual(cabinet.get_materials()[1]['part'].name, 'cabinet_bottom')
        self.assertEqual(cabinet.get_materials()[2]['part'].name, 'drawer_screw')
        self.assertEqual(cabinet.get_materials()[3]['part'].name, 'drawer_panel')
        self.assertEqual(len(cabinet.get_materials()), 4)

    def test_get_object(self):
        part = Part()
        with self.assertRaises(NotImplementedError):
            part.get_object()

    def test_get_params(self):
        self.assertEqual(Part().get_params(), collections.OrderedDict([('name', '')]))
        self.assertEqual(Part(name='drawer').get_params(), collections.OrderedDict([('name', 'drawer')]))
