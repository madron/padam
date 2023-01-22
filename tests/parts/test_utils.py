import unittest
from padam.parts.frame import Frame
from padam import utils


class PanelListTest(unittest.TestCase):
    def test_material(self):
        frame = Frame(name='kitchen', length=1200, height=700, depth=600, thickness=20, material='plywood')
        panels = utils.get_panel_list(frame)
        self.assertEqual(len(panels), 4)
        panel = panels[0]
        self.assertEqual(panel['label'], 'top_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 1160)
        self.assertEqual(panel['width'], 600)
        panel = panels[1]
        self.assertEqual(panel['label'], 'bottom_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 1160)
        self.assertEqual(panel['width'], 600)
        panel = panels[2]
        self.assertEqual(panel['label'], 'left_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 700)
        self.assertEqual(panel['width'], 600)
        panel = panels[3]
        self.assertEqual(panel['label'], 'right_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 700)
        self.assertEqual(panel['width'], 600)

    def test_no_material(self):
        frame = Frame(name='kitchen', length=1200, height=700, depth=600, thickness=20)
        panels = utils.get_panel_list(frame)
        self.assertEqual(len(panels), 4)
        panel = panels[0]
        self.assertEqual(panel['label'], 'top_panel')
        self.assertEqual(panel['material'], '20')
        self.assertEqual(panel['length'], 1160)
        self.assertEqual(panel['width'], 600)
        panel = panels[1]
        self.assertEqual(panel['label'], 'bottom_panel')
        self.assertEqual(panel['material'], '20')
        self.assertEqual(panel['length'], 1160)
        self.assertEqual(panel['width'], 600)
        panel = panels[2]
        self.assertEqual(panel['label'], 'left_panel')
        self.assertEqual(panel['material'], '20')
        self.assertEqual(panel['length'], 700)
        self.assertEqual(panel['width'], 600)
        panel = panels[3]
        self.assertEqual(panel['label'], 'right_panel')
        self.assertEqual(panel['material'], '20')
        self.assertEqual(panel['length'], 700)
        self.assertEqual(panel['width'], 600)
