import unittest
from padam.parts import Part


class PartTest(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Part(name='mypart')), 'mypart')

    def test_no_parts(self):
        part = Part()
        self.assertEqual(part.parts, [])
        self.assertEqual(part.materials, [part])

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
        self.assertEqual(panel.materials[0].name, 'screw 1')
        self.assertEqual(panel.materials[1].name, 'screw 2')
        self.assertEqual(len(panel.materials), 2)

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
        self.assertEqual(cabinet.materials[0].name, 'cabinet_top')
        self.assertEqual(cabinet.materials[1].name, 'cabinet_bottom')
        self.assertEqual(cabinet.materials[2].name, 'drawer_screw')
        self.assertEqual(cabinet.materials[3].name, 'drawer_panel')
        self.assertEqual(len(cabinet.materials), 4)
