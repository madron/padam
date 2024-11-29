import unittest
from padam.parts.frame import Frame
from padam import utils


class PanelListTest(unittest.TestCase):
    def test_material(self):
        frame = Frame(name='kitchen', length=1200, height=700, depth=600, thickness=20, material='plywood')
        panels = utils.get_panel_list(frame)
        self.assertEqual(len(panels), 4)
        panel = panels[0]
        self.assertEqual(panel['label'], 'kitchen_top_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 1160)
        self.assertEqual(panel['width'], 600)
        panel = panels[1]
        self.assertEqual(panel['label'], 'kitchen_bottom_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 1160)
        self.assertEqual(panel['width'], 600)
        panel = panels[2]
        self.assertEqual(panel['label'], 'kitchen_left_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 700)
        self.assertEqual(panel['width'], 600)
        panel = panels[3]
        self.assertEqual(panel['label'], 'kitchen_right_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 700)
        self.assertEqual(panel['width'], 600)

    def test_no_material(self):
        frame = Frame(name='kitchen', length=1200, height=700, depth=600, thickness=20)
        panels = utils.get_panel_list(frame)
        self.assertEqual(len(panels), 4)
        panel = panels[0]
        self.assertEqual(panel['label'], 'kitchen_top_panel')
        self.assertEqual(panel['material'], '20')
        self.assertEqual(panel['length'], 1160)
        self.assertEqual(panel['width'], 600)
        panel = panels[1]
        self.assertEqual(panel['label'], 'kitchen_bottom_panel')
        self.assertEqual(panel['material'], '20')
        self.assertEqual(panel['length'], 1160)
        self.assertEqual(panel['width'], 600)
        panel = panels[2]
        self.assertEqual(panel['label'], 'kitchen_left_panel')
        self.assertEqual(panel['material'], '20')
        self.assertEqual(panel['length'], 700)
        self.assertEqual(panel['width'], 600)
        panel = panels[3]
        self.assertEqual(panel['label'], 'kitchen_right_panel')
        self.assertEqual(panel['material'], '20')
        self.assertEqual(panel['length'], 700)
        self.assertEqual(panel['width'], 600)


class CutListTest(unittest.TestCase):
    def test_material(self):
        frame = Frame(name='kitchen', length=1200, height=700, depth=600, thickness=20, material='plywood')
        cut_list = utils.get_cutlist(frame)
        lines = cut_list.splitlines()
        self.assertEqual(lines[0], 'Length,Width,Qty,Material,Label,Enabled,Grain direction')
        self.assertEqual(lines[1], '1160.0,600.0,1,plywood_20,kitchen_top_panel,true,v')
        self.assertEqual(lines[2], '1160.0,600.0,1,plywood_20,kitchen_bottom_panel,true,v')
        self.assertEqual(lines[3], '700.0,600.0,1,plywood_20,kitchen_left_panel,true,v')
        self.assertEqual(lines[4], '700.0,600.0,1,plywood_20,kitchen_right_panel,true,v')
        self.assertEqual(len(lines), 5)

    def test_material_no_name(self):
        frame = Frame(length=1200, height=700, depth=600, thickness=20, material='plywood')
        cut_list = utils.get_cutlist(frame)
        lines = cut_list.splitlines()
        self.assertEqual(lines[0], 'Length,Width,Qty,Material,Label,Enabled,Grain direction')
        self.assertEqual(lines[1], '1160.0,600.0,1,plywood_20,top_panel,true,v')
        self.assertEqual(lines[2], '1160.0,600.0,1,plywood_20,bottom_panel,true,v')
        self.assertEqual(lines[3], '700.0,600.0,1,plywood_20,left_panel,true,v')
        self.assertEqual(lines[4], '700.0,600.0,1,plywood_20,right_panel,true,v')
        self.assertEqual(len(lines), 5)
