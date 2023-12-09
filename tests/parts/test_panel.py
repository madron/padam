import unittest
from solid import cube
from padam.parts.panel import Panel


class PanelTest(unittest.TestCase):
    def test_str(self):
        panel = Panel(1000, 30, 18, name='bottom')
        self.assertEqual(str(panel), 'bottom')

    def test_parts(self):
        panel = Panel(1000, 30, 18)
        self.assertEqual(panel.parts, [])

    def test_materials(self):
        panel = Panel(1000, 30, 18)
        self.assertEqual(panel.materials,  [dict(names=[], part=panel)])

    def test_get_object(self):
        obj = Panel(1000, 200, 18, name='panel').get_object()
        self.assertIsInstance(obj, cube)
        self.assertEqual(obj.params['size'], [1000, 200, 18])

    def test_get_objects(self):
        objs = Panel(1000, 200, 18, name='panel').get_objects()
        self.assertEqual(len(objs), 1)

    def test_get_params(self):
        panel = Panel(1000, 150, 25, name='bottom', material='plywood')
        params = panel.get_params()
        self.assertEqual(len(params), 5)
        self.assertEqual(params['name'], 'bottom')
        self.assertEqual(params['material'], 'plywood')
        self.assertEqual(params['length'], 1000)
        self.assertEqual(params['width'], 150)
        self.assertEqual(params['thickness'], 25)

    def test_get_panel_cut(self):
        panel = Panel(1000, 30, 18, material='plywood').get_panel_cut()
        self.assertEqual(panel['material'], 'plywood')
        self.assertEqual(panel['length'], 1000)
        self.assertEqual(panel['width'], 30)
        self.assertEqual(panel['thickness'], 18)
