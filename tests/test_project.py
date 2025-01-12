import unittest
from collections import OrderedDict
from padam.parts import Cabinet, Panel, BasePanel
from padam.project import get_parameter, get_default, get_part
from padam.project import Project


class ProjectTest(unittest.TestCase):
    def test_empty(self):
        project = Project()
        self.assertEqual(project.default, dict())

    def test_default(self):
        default=dict(
            cabinet=dict(
                thickness=18,
            ),
        )
        project = Project(default=default)
        self.assertEqual(project.default, default)

    def test_default_inherits(self):
        default=dict(
            cabinet=dict(
                thickness=18,
            ),
            cabinet_top=dict(
                inherits='cabinet',
                depth=400,
            ),
        )
        project = Project(default=default)
        self.assertEqual(project.default['cabinet']['thickness'], 18)
        self.assertEqual(project.default['cabinet_top']['thickness'], 18)
        self.assertEqual(project.default['cabinet_top']['depth'], 400)

    def test_default_inherits_wrong_parent(self):
        default=dict(
            cabinet=dict(
                thickness=18,
            ),
            cabinet_top=dict(
                inherits='wrong',
                depth=400,
            ),
        )
        with self.assertRaises(ValueError) as cm:
            Project(default=default)
        errors = cm.exception.errors()
        self.assertEqual(errors[0]['loc'], ('default',))
        self.assertEqual(errors[0]['msg'], 'Value error, section "cabinet_top" inherits from non existent section "wrong"')
        self.assertEqual(len(errors), 1)

    def test_part_base(self):
        default=dict(
            cabinet=dict(
                thickness=19,
                depth=600,
            ),
        )
        part = dict(
            base=dict(type='cabinet', default='cabinet', length=800),
        )
        project = Project(default=default, part=part)
        self.assertEqual(project.default['cabinet']['thickness'], 19)
        self.assertEqual(project.default['cabinet']['depth'], 600)
        self.assertEqual(len(project.default['cabinet']), 2)
        self.assertEqual(len(project.default), 1)
        cabinet: Cabinet = project.part['base']
        self.assertEqual(cabinet.name, 'base')
        self.assertEqual(cabinet.thickness, 19)
        self.assertEqual(cabinet.length, 800)
        self.assertEqual(cabinet.depth, 600)
        self.assertEqual(len(project.part), 1)

    def test_no_default(self):
        part = dict(
            base=dict(type='cabinet', default='cabinet', length=800, depth=600, thickness=19),
        )
        project = Project(part=part)
        self.assertEqual(project.default, dict())
        cabinet: Cabinet = project.part['base']
        self.assertEqual(cabinet.name, 'base')
        self.assertEqual(cabinet.length, 800)
        self.assertEqual(cabinet.depth, 600)
        self.assertEqual(cabinet.thickness, 19)
        self.assertEqual(len(project.part), 1)

    def test_get_objects(self):
        part = dict(
            shelf1=dict(type='panel', length=800, width=250, thickness=18),
            shelf2=dict(type='panel', length=1200, width=250, thickness=18),
        )
        project = Project(part=part)
        objs = project.get_objects()
        self.assertEqual(len(objs), 2)

    def test_get_materials(self):
        shelf1_dict = dict(type='panel', length=800, width=250, thickness=18)
        shelf2_dict = dict(type='panel', length=1200, width=250, thickness=18)
        part = dict(shelf1=shelf1_dict, shelf2=shelf2_dict)
        project = Project(part=part)
        materials = project.get_materials()
        material = materials[0]
        self.assertEqual(material, dict(names=['shelf1'], part=BasePanel(name='shelf1', **shelf1_dict)))
        material = materials[1]
        self.assertEqual(material, dict(names=['shelf2'], part=BasePanel(name='shelf2', **shelf2_dict)))
        self.assertEqual(len(materials), 2)

    def test_get_materials_no_part(self):
        project = Project()
        materials = project.get_materials()
        self.assertEqual(len(materials), 0)


class GetParameterTest(unittest.TestCase):
    def test_empty(self):
        data = OrderedDict()
        parameter = get_parameter(data)
        self.assertEqual(parameter, dict())

    def test_int(self):
        data = OrderedDict(length=800)
        parameter = get_parameter(data)
        self.assertEqual(parameter, dict(length=800))

    def test_text_int(self):
        data = OrderedDict(length='800')
        parameter = get_parameter(data)
        self.assertEqual(parameter, dict(length=800))

    def test_float(self):
        data = OrderedDict(length='float(800)')
        parameter = get_parameter(data)
        self.assertEqual(parameter, dict(length=800.0))

    def test_simple_calculation(self):
        data = OrderedDict(length='10 + 15')
        parameter = get_parameter(data)
        self.assertEqual(parameter, dict(length=25))

    def test_calculation_1(self):
        data = OrderedDict(
            part1=10,
            part2=15,
            total='part1 + part2',
        )
        parameter = get_parameter(data)
        self.assertEqual(parameter['part1'], 10)
        self.assertEqual(parameter['part2'], 15)
        self.assertEqual(parameter['total'], 25)

    def test_calculation_2(self):
        data = OrderedDict(
            part1=10,
            part2=15,
            total='(part1 + part2 * 2) / 2',
        )
        parameter = get_parameter(data)
        self.assertEqual(parameter['total'], 20)

    def test_missing_parameter(self):
        data = OrderedDict(
            part1=10,
            part3=15,
            total='part1 + part2',
        )
        with self.assertRaises(ValueError) as cm:
            get_parameter(data)
        errors = cm.exception.args
        self.assertEqual(errors, ("error in 'total': name 'part2' is not defined",))

class GetDefaultTest(unittest.TestCase):
    def test_inherits_3_levels(self):
        data=dict(
            d1=dict(
                d1=1,
            ),
            d3=dict(
                inherits='d2',
                d3=3,
            ),
            d2=dict(
                inherits='d1',
                d2=2,
            ),
        )
        default = get_default(data)
        self.assertEqual(default['d1'], dict(d1=1))
        self.assertEqual(default['d2'], dict(d1=1, d2=2))
        self.assertEqual(default['d3'], dict(d1=1, d2=2, d3=3))

    def test_inherits_4_levels(self):
        data=dict(
            d4=dict(
                inherits='d3',
                d4=4,
            ),
            d1=dict(
                d1=1,
            ),
            d3=dict(
                inherits='d2',
                d3=3,
            ),
            d2=dict(
                inherits='d1',
                d2=2,
            ),
        )
        default = get_default(data)
        self.assertEqual(default['d1'], dict(d1=1))
        self.assertEqual(default['d2'], dict(d1=1, d2=2))
        self.assertEqual(default['d3'], dict(d1=1, d2=2, d3=3))
        self.assertEqual(default['d4'], dict(d1=1, d2=2, d3=3, d4=4))


class GetPartTest(unittest.TestCase):
    def test_empty(self):
        default=dict(
            cabinet=dict(thickness=18),
        )
        data = dict()
        part = get_part(data, default)
        self.assertEqual(part, dict())

    def test_1_base(self):
        default=dict(
            base=dict(thickness=22),
        )
        data = dict(
            base=dict(type='cabinet', default='base'),
        )
        part = get_part(data, default)
        cabinet: Cabinet = part['base']
        self.assertIsInstance(cabinet, Cabinet)
        self.assertEqual(cabinet.thickness, 22)
        self.assertEqual(len(part), 1)

    def test_2_base(self):
        default=dict(
            base=dict(thickness=25),
        )
        data = dict(
            base1=dict(type='cabinet', default='base', length=800),
            base2=dict(type='cabinet', default='base', length=600),
        )
        part = get_part(data, default)
        cabinet: Cabinet = part['base1']
        self.assertIsInstance(cabinet, Cabinet)
        self.assertEqual(cabinet.thickness, 25)
        self.assertEqual(cabinet.length, 800)
        cabinet: Cabinet = part['base2']
        self.assertIsInstance(cabinet, Cabinet)
        self.assertEqual(cabinet.thickness, 25)
        self.assertEqual(cabinet.length, 600)
        self.assertEqual(len(part), 2)

    def test_2_base_2_top_1shelf(self):
        default = dict(
            cabinet=dict(
                material='plywood',
                thickness=18,
            ),
            cabinet_base=dict(
                material='plywood',
                thickness=18,
                depth=600,
                height=700,
                door_number=1,
            ),
            cabinet_top=dict(
                material='plywood',
                thickness=18,
                depth=400,
                height=600,
                door_number=1,
            ),
        )
        data = dict(
            shelf=dict(
                type='panel',
                default='cabinet',
                length=1600,
                width=250,
            ),
            base1=dict(
                type='cabinet',
                default='cabinet_base',
                length=800,
                door_number=2,
            ),
            base2=dict(
                type='cabinet',
                default='cabinet_base',
                length=600,
            ),
            top1=dict(
                type='cabinet',
                default='cabinet_top',
                length=800,
                door_number=2,
            ),
            top2=dict(
                type='cabinet',
                default='cabinet_top',
                length=600,
            ),
        )
        part = get_part(data, default)
        panel: Panel = part['shelf']
        self.assertIsInstance(panel, Panel)
        self.assertEqual(panel.material, 'plywood')
        self.assertEqual(panel.length, 1600)
        self.assertEqual(panel.width, 250)
        self.assertEqual(panel.thickness, 18)
        cabinet: Cabinet = part['top1']
        self.assertIsInstance(cabinet, Cabinet)
        self.assertEqual(cabinet.material, 'plywood')
        self.assertEqual(cabinet.thickness, 18)
        self.assertEqual(cabinet.length, 800)
        self.assertEqual(cabinet.depth, 400)
        cabinet: Cabinet = part['top2']
        self.assertIsInstance(cabinet, Cabinet)
        self.assertEqual(cabinet.material, 'plywood')
        self.assertEqual(cabinet.thickness, 18)
        self.assertEqual(cabinet.length, 600)
        self.assertEqual(cabinet.depth, 400)
        cabinet: Cabinet = part['base1']
        self.assertIsInstance(cabinet, Cabinet)
        self.assertEqual(cabinet.material, 'plywood')
        self.assertEqual(cabinet.thickness, 18)
        self.assertEqual(cabinet.length, 800)
        self.assertEqual(cabinet.depth, 600)
        cabinet: Cabinet = part['base2']
        self.assertIsInstance(cabinet, Cabinet)
        self.assertEqual(cabinet.material, 'plywood')
        self.assertEqual(cabinet.thickness, 18)
        self.assertEqual(cabinet.length, 600)
        self.assertEqual(cabinet.depth, 600)
        self.assertEqual(len(part), 5)
