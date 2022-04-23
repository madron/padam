import unittest
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
        self.assertEqual(panel.materials, [panel])

    def test_get_object(self):
        obj = Panel(1000, 200, 18, name='panel').get_object()
        self.assertEqual(obj.Length.toStr(), '1000.00 mm')
        self.assertEqual(obj.Width.toStr(), '200.00 mm')
        self.assertEqual(obj.Height.toStr(), '18.00 mm')
        self.assertEqual(obj.Label, 'panel')
