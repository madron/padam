import unittest
from padam.parts.panel import Panel
try:
    import cadquery as cq
    cadquery_missing = False
except:  # pragma: no cover
    cadquery_missing = 'cadquery module not available'


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

    @unittest.skipIf(cadquery_missing, cadquery_missing)
    def test_get_object(self):
        obj = Panel(1000, 30, 18).get_object()
        self.assertIsInstance(obj, cq.Workplane)
