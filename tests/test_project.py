import unittest
from padam.project import get_default
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

    def test_inherits(self):
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

    def test_inherits_wrong_parent(self):
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
