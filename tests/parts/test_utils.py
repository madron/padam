import unittest
from padam.parts.frame import Frame
from padam import Project
from padam import utils


class PanelListTest(unittest.TestCase):
    def test_material(self):
        project = Project(part=dict(kitchen=dict(type='frame', length=1200, height=700, depth=600, thickness=20, material='plywood')))
        panels = utils.get_panel_list(project)
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

    def test_material_2(self):
        project = Project(part=dict(
            base1=dict(type='frame', length=1200, height=700, depth=600, thickness=20, material='plywood'),
            base2=dict(type='frame', length=800, height=700, depth=600, thickness=20, material='plywood'),
        ))
        panels = utils.get_panel_list(project)
        self.assertEqual(len(panels), 8)
        panel = panels[0]
        self.assertEqual(panel['label'], 'base1_top_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 1160)
        self.assertEqual(panel['width'], 600)
        panel = panels[1]
        self.assertEqual(panel['label'], 'base1_bottom_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 1160)
        self.assertEqual(panel['width'], 600)
        panel = panels[2]
        self.assertEqual(panel['label'], 'base1_left_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 700)
        self.assertEqual(panel['width'], 600)
        panel = panels[3]
        self.assertEqual(panel['label'], 'base1_right_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 700)
        self.assertEqual(panel['width'], 600)
        panel = panels[4]
        self.assertEqual(panel['label'], 'base2_top_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 760)
        self.assertEqual(panel['width'], 600)
        panel = panels[5]
        self.assertEqual(panel['label'], 'base2_bottom_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 760)
        self.assertEqual(panel['width'], 600)
        panel = panels[6]
        self.assertEqual(panel['label'], 'base2_left_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 700)
        self.assertEqual(panel['width'], 600)
        panel = panels[7]
        self.assertEqual(panel['label'], 'base2_right_panel')
        self.assertEqual(panel['material'], 'plywood_20')
        self.assertEqual(panel['length'], 700)
        self.assertEqual(panel['width'], 600)

    def test_no_material(self):
        project = Project(part=dict(kitchen=dict(type='frame', length=1200, height=700, depth=600, thickness=20)))
        panels = utils.get_panel_list(project)
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
        project = Project(part=dict(kitchen=dict(type='frame', length=1200, height=700, depth=600, thickness=20, material='plywood')))
        cut_list = utils.get_cutlist(project)
        lines = cut_list.splitlines()
        self.assertEqual(lines[0], 'Length,Width,Qty,Material,Label,Enabled,Grain direction')
        self.assertEqual(lines[1], '1160.0,600.0,1,plywood_20,kitchen_top_panel,true,v')
        self.assertEqual(lines[2], '1160.0,600.0,1,plywood_20,kitchen_bottom_panel,true,v')
        self.assertEqual(lines[3], '700.0,600.0,1,plywood_20,kitchen_left_panel,true,v')
        self.assertEqual(lines[4], '700.0,600.0,1,plywood_20,kitchen_right_panel,true,v')
        self.assertEqual(len(lines), 5)

    def test_material_2(self):
        project = Project(part=dict(
            base1=dict(type='frame', length=1200, height=700, depth=600, thickness=20, material='plywood'),
            base2=dict(type='frame', length=800, height=700, depth=600, thickness=20, material='plywood'),
        ))
        cut_list = utils.get_cutlist(project)
        lines = cut_list.splitlines()
        self.assertEqual(lines[0], 'Length,Width,Qty,Material,Label,Enabled,Grain direction')
        self.assertEqual(lines[1], '1160.0,600.0,1,plywood_20,base1_top_panel,true,v')
        self.assertEqual(lines[2], '1160.0,600.0,1,plywood_20,base1_bottom_panel,true,v')
        self.assertEqual(lines[3], '700.0,600.0,1,plywood_20,base1_left_panel,true,v')
        self.assertEqual(lines[4], '700.0,600.0,1,plywood_20,base1_right_panel,true,v')
        self.assertEqual(lines[5], '760.0,600.0,1,plywood_20,base2_top_panel,true,v')
        self.assertEqual(lines[6], '760.0,600.0,1,plywood_20,base2_bottom_panel,true,v')
        self.assertEqual(lines[7], '700.0,600.0,1,plywood_20,base2_left_panel,true,v')
        self.assertEqual(lines[8], '700.0,600.0,1,plywood_20,base2_right_panel,true,v')
        self.assertEqual(len(lines), 9)

