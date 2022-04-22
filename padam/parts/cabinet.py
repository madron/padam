from typing import Optional
import cadquery as cq


class Cabinet:
    def __init__(
        self,
        length: Optional[int] = 1200,
        height: Optional[int] = 700,
        depth: Optional[int] = 600,
        thickness: Optional[int] = 18,
        top_thickness: Optional[int] = None,
        bottom_thickness: Optional[int] = None,
        side_thickness: Optional[int] = None,
        top_slitted: Optional[bool] = True,
        top_front_depth: Optional[int] = 100,
        top_back_depth: Optional[int] = 100,
    ):
        self.length = length
        self.height = height
        self.depth = depth
        self.top_thickness = top_thickness or thickness
        self.bottom_thickness = bottom_thickness or thickness
        self.side_thickness = side_thickness or thickness
        self.top_slitted = top_slitted
        self.top_front_depth = top_front_depth
        self.top_back_depth = top_back_depth

    def get_interior_length(self):
        return self.length - 2 * self.side_thickness

    def get_top_panel(self):
        return cq.Workplane().box(self.get_interior_length(), self.depth, self.top_thickness)

    def get_top_front_panel(self):
        return cq.Workplane().box(self.get_interior_length(), self.top_front_depth, self.top_thickness)

    def get_top_back_panel(self):
        return cq.Workplane().box(self.get_interior_length(), self.top_back_depth, self.top_thickness)

    def get_bottom_panel(self):
        panel =  cq.Workplane().box(self.get_interior_length(), self.depth, self.bottom_thickness)
        panel.faces('>Z').tag('top_face')
        panel.faces('<Z').tag('bottom_face')
        panel.faces('<Y').tag('left_face')
        panel.faces('>Y').tag('right_face')
        panel.edges('|Y and <X and <Z').tag('bottom_left_edge')
        panel.edges('|Y and >X and <Z').tag('bottom_right_edge')
        panel.vertices('<X and <Y and <Z').tag('bottom_front_left_vertex')
        panel.vertices('<X and >Y and <Z').tag('bottom_back_left_vertex')
        return panel

    def get_side_panel(self):
        panel = cq.Workplane().box(self.side_thickness, self.depth, self.height, )
        panel.faces('>Z').tag('top_face')
        panel.faces('<Z').tag('bottom_face')
        panel.edges('|Y and <X and <Z').tag('bottom_left_edge')
        panel.edges('|Y and >X and <Z').tag('bottom_right_edge')
        panel.vertices('<X and <Y and <Z').tag('bottom_front_left_vertex')
        panel.vertices('>X and >Y and <Z').tag('bottom_back_right_vertex')
        return panel

    def get_obj(self):
        a = cq.Assembly()
        # bottom
        bottom_panel = self.get_bottom_panel()
        a.add(
            bottom_panel,
            name='bottom_panel',
            loc=cq.Location(cq.Vector(self.get_interior_length() / 2 + self.side_thickness, self.depth / 2, self.bottom_thickness / 2)),
            color=cq.Color('burlywood'),
        )
        # left
        left_panel = self.get_side_panel()
        a.add(
            left_panel,
            name='left_panel',
            loc=cq.Location(cq.Vector(self.side_thickness / 2, self.depth / 2, self.height / 2)),
            color=cq.Color('burlywood'),
        )
        # right
        right_panel = self.get_side_panel()
        a.add(
            right_panel,
            name='right_panel',
            loc=cq.Location(cq.Vector(- self.side_thickness / 2 + self.length, self.depth / 2, self.height / 2)),
            color=cq.Color('burlywood'),
        )
        return a
