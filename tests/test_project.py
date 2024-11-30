import unittest
from padam.parts import Cabinet, Panel
from padam.project import get_default, get_part
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

    def test_get_objects(self):
        part = dict(
            shelf1=dict(type='panel', length=800, width=250, thickness=18),
            shelf2=dict(type='panel', length=1200, width=250, thickness=18),
        )
        project = Project(part=part)
        objs = project.get_objects()
        self.assertEqual(len(objs), 2)


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
