import io
import contextlib
import unittest
from pydantic import ValidationError
from solid import color, cube
from padam.parts.panel import EdgeBandedPanel, Panel


class PanelTest(unittest.TestCase):
    def test_str(self):
        panel = Panel(1000, 30, 18, name='bottom')
        self.assertEqual(str(panel), 'bottom')

    def test_default(self):
        default = dict(
            material='plywood',
            width=400,
            thickness=18,
        )
        panel = Panel(1000, default=default)
        self.assertEqual(panel.length, 1000)
        self.assertEqual(panel.width, 400)
        self.assertEqual(panel.thickness, 18)
        self.assertEqual(panel.material, 'plywood')

    def test_default_not_inexisting_field(self):
        default = dict(wrong_field='no problem')
        panel = Panel(1000, 30, 18, default=default)
        self.assertEqual(panel.length, 1000)
        self.assertEqual(panel.width, 30)
        self.assertEqual(panel.thickness, 18)
        self.assertEqual(panel.material, '')

    def test_default_wrong_material(self):
        default = dict(material=20)
        with self.assertRaises(ValidationError) as cm:
            Panel(1000, 30, 18, default=default)
        errors = cm.exception.errors()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['loc'], ('material',))
        self.assertEqual(errors[0]['msg'], 'Input should be a valid string')

    def test_default_wrong_length(self):
        default = dict(length='200 mm')
        with self.assertRaises(ValidationError) as cm:
            Panel(width=400, thickness=18, default=default)
        errors = cm.exception.errors()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['loc'], ('length',))
        self.assertEqual(errors[0]['msg'], 'Input should be a valid number, unable to parse string as a number')

    def test_default_missing_thickness(self):
        default = dict(material='plywood')
        with self.assertRaises(ValidationError) as cm:
            Panel(1000, 30, default=default)
        errors = cm.exception.errors()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['loc'], ('thickness',))
        self.assertEqual(errors[0]['msg'], 'Input should be a valid number')

    def test_cut_oversize(self):
        panel = Panel(1000, 30, 18)
        self.assertEqual(panel.cut_length_oversize, 0)
        self.assertEqual(panel.cut_width_oversize, 0)
        self.assertEqual(panel.cut_thickness_oversize, 0)

    def test_cut_oversize_default(self):
        default = dict(
            cut_length_oversize=5,
            cut_width_oversize=4,
            cut_thickness_oversize=3,
        )
        panel = Panel(1000, 30, 18, default=default)
        self.assertEqual(panel.cut_length_oversize, 5)
        self.assertEqual(panel.cut_width_oversize, 4)
        self.assertEqual(panel.cut_thickness_oversize, 3)

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

    def test_get_object_color(self):
        obj = Panel(1000, 200, 18, name='panel', material='plywood').get_object()
        self.assertIsInstance(obj, color)

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

    def test_run(self):
        output = io.StringIO()
        cutlist = io.StringIO()
        with io.StringIO() as buf:
            with contextlib.redirect_stdout(buf):
                Panel(1000, 30, 18).run(output=output, cutlist=cutlist)


class EdgeBandedPanelTest(unittest.TestCase):
    def test_str(self):
        panel = EdgeBandedPanel(
            length=1000,
            width=30,
            thickness=18,
            name='bottom',
            front_edge_banding_thickness=10,
            back_edge_banding_thickness=10,
            left_edge_banding_thickness=10,
            right_edge_banding_thickness=10,
            edge_banding_material='hardwood',
            edge_banding_style='length',
        )
        self.assertEqual(str(panel), 'bottom')

    def test_parts_length(self):
        panel = EdgeBandedPanel(
            length=1000,
            width=200,
            thickness=18,
            name='bottom',
            material='plywood',
            front_edge_banding_thickness=10,
            back_edge_banding_thickness=10,
            left_edge_banding_thickness=10,
            right_edge_banding_thickness=10,
            edge_banding_material='hardwood',
            edge_banding_style='length',
        )
        self.assertEqual(len(panel.parts), 5)
        # Front
        part = panel.parts[0]
        self.assertEqual(part.length, 1000)
        self.assertEqual(part.width, 10)
        self.assertEqual(part.thickness, 18)
        self.assertEqual(part.material, 'hardwood')
        self.assertEqual(part.name, 'front_edge')
        # back
        part = panel.parts[1]
        self.assertEqual(part.length, 1000)
        self.assertEqual(part.width, 10)
        self.assertEqual(part.thickness, 18)
        self.assertEqual(part.material, 'hardwood')
        self.assertEqual(part.name, 'back_edge')
        # left
        part = panel.parts[2]
        self.assertEqual(part.length, 180)
        self.assertEqual(part.width, 10)
        self.assertEqual(part.thickness, 18)
        self.assertEqual(part.material, 'hardwood')
        self.assertEqual(part.name, 'left_edge')
        # right
        part = panel.parts[3]
        self.assertEqual(part.length, 180)
        self.assertEqual(part.width, 10)
        self.assertEqual(part.thickness, 18)
        self.assertEqual(part.material, 'hardwood')
        self.assertEqual(part.name, 'right_edge')
        # Main panel
        part = panel.parts[4]
        self.assertEqual(part.length, 980)
        self.assertEqual(part.width, 180)
        self.assertEqual(part.thickness, 18)
        self.assertEqual(part.material, 'plywood')
        self.assertEqual(part.name, None)

    def test_parts_width(self):
        panel = EdgeBandedPanel(
            length=1000,
            width=200,
            thickness=18,
            name='bottom',
            material='plywood',
            front_edge_banding_thickness=10,
            back_edge_banding_thickness=10,
            left_edge_banding_thickness=10,
            right_edge_banding_thickness=10,
            edge_banding_material='hardwood',
            edge_banding_style='width',
        )
        self.assertEqual(len(panel.parts), 5)
        # Front
        part = panel.parts[0]
        self.assertEqual(part.length, 980)
        self.assertEqual(part.width, 10)
        self.assertEqual(part.thickness, 18)
        self.assertEqual(part.material, 'hardwood')
        self.assertEqual(part.name, 'front_edge')
        # back
        part = panel.parts[1]
        self.assertEqual(part.length, 980)
        self.assertEqual(part.width, 10)
        self.assertEqual(part.thickness, 18)
        self.assertEqual(part.material, 'hardwood')
        self.assertEqual(part.name, 'back_edge')
        # left
        part = panel.parts[2]
        self.assertEqual(part.length, 200)
        self.assertEqual(part.width, 10)
        self.assertEqual(part.thickness, 18)
        self.assertEqual(part.material, 'hardwood')
        self.assertEqual(part.name, 'left_edge')
        # right
        part = panel.parts[3]
        self.assertEqual(part.length, 200)
        self.assertEqual(part.width, 10)
        self.assertEqual(part.thickness, 18)
        self.assertEqual(part.material, 'hardwood')
        self.assertEqual(part.name, 'right_edge')
        # Main panel
        part = panel.parts[4]
        self.assertEqual(part.length, 980)
        self.assertEqual(part.width, 180)
        self.assertEqual(part.thickness, 18)
        self.assertEqual(part.material, 'plywood')
        self.assertEqual(part.name, None)

    def test_parts_overlap(self):
        panel = EdgeBandedPanel(
            length=1000,
            width=200,
            thickness=18,
            name='bottom',
            material='plywood',
            front_edge_banding_thickness=10,
            back_edge_banding_thickness=10,
            left_edge_banding_thickness=10,
            right_edge_banding_thickness=10,
            edge_banding_material='hardwood',
            edge_banding_style='overlap',
        )
        self.assertEqual(len(panel.parts), 5)
        # Front
        part = panel.parts[0]
        self.assertEqual(part.length, 1000)
        self.assertEqual(part.width, 10)
        self.assertEqual(part.thickness, 18)
        self.assertEqual(part.material, 'hardwood')
        self.assertEqual(part.name, 'front_edge')
        # back
        part = panel.parts[1]
        self.assertEqual(part.length, 1000)
        self.assertEqual(part.width, 10)
        self.assertEqual(part.thickness, 18)
        self.assertEqual(part.material, 'hardwood')
        self.assertEqual(part.name, 'back_edge')
        # left
        part = panel.parts[2]
        self.assertEqual(part.length, 200)
        self.assertEqual(part.width, 10)
        self.assertEqual(part.thickness, 18)
        self.assertEqual(part.material, 'hardwood')
        self.assertEqual(part.name, 'left_edge')
        # right
        part = panel.parts[3]
        self.assertEqual(part.length, 200)
        self.assertEqual(part.width, 10)
        self.assertEqual(part.thickness, 18)
        self.assertEqual(part.material, 'hardwood')
        self.assertEqual(part.name, 'right_edge')
        # Main panel
        part = panel.parts[4]
        self.assertEqual(part.length, 980)
        self.assertEqual(part.width, 180)
        self.assertEqual(part.thickness, 18)
        self.assertEqual(part.material, 'plywood')
        self.assertEqual(part.name, None)

    def test_materials(self):
        panel = EdgeBandedPanel(
            length=1000,
            width=30,
            thickness=18,
            name='bottom',
            front_edge_banding_thickness=10,
            back_edge_banding_thickness=10,
            left_edge_banding_thickness=10,
            right_edge_banding_thickness=10,
            edge_banding_material='hardwood',
            edge_banding_style='length',
        )
        # self.assertEqual(panel.materials,  [dict(names=[], part=panel)])
        # Front
        material = panel.materials[0]
        self.assertEqual(material['names'], ['bottom', 'front_edge'])
        self.assertIsInstance(material['part'], Panel)
        # back
        material = panel.materials[1]
        self.assertEqual(material['names'], ['bottom', 'back_edge'])
        self.assertIsInstance(material['part'], Panel)
        # left
        material = panel.materials[2]
        self.assertEqual(material['names'], ['bottom', 'left_edge'])
        self.assertIsInstance(material['part'], Panel)
        # right
        material = panel.materials[3]
        self.assertEqual(material['names'], ['bottom', 'right_edge'])
        self.assertIsInstance(material['part'], Panel)
        # Main panel
        material = panel.materials[4]
        self.assertEqual(material['names'], ['bottom'])
        self.assertIsInstance(material['part'], Panel)

    def test_get_objects_length(self):
        panel = EdgeBandedPanel(
            length=1000,
            width=30,
            thickness=18,
            name='bottom',
            front_edge_banding_thickness=10,
            back_edge_banding_thickness=10,
            left_edge_banding_thickness=10,
            right_edge_banding_thickness=10,
            edge_banding_material='hardwood',
            edge_banding_style='length',
        )
        objs = panel.get_objects()
        self.assertEqual(len(objs), 5)

    def test_get_objects_width(self):
        panel = EdgeBandedPanel(
            length=1000,
            width=30,
            thickness=18,
            name='bottom',
            front_edge_banding_thickness=10,
            back_edge_banding_thickness=10,
            left_edge_banding_thickness=10,
            right_edge_banding_thickness=10,
            edge_banding_material='hardwood',
            edge_banding_style='width',
        )
        objs = panel.get_objects()
        self.assertEqual(len(objs), 5)

    def test_get_params(self):
        panel = EdgeBandedPanel(
            length=1000,
            width=200,
            thickness=18,
            name='bottom',
            material='plywood',
            front_edge_banding_thickness=10,
            back_edge_banding_thickness=10,
            left_edge_banding_thickness=10,
            right_edge_banding_thickness=10,
            edge_banding_material='hardwood',
            edge_banding_style='length',
        )
        params = panel.get_params()
        self.assertEqual(len(params), 5)
        self.assertEqual(params['name'], 'bottom')
        self.assertEqual(params['material'], 'plywood')
        self.assertEqual(params['length'], 1000)
        self.assertEqual(params['width'], 200)
        self.assertEqual(params['thickness'], 18)
