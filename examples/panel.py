from padam.parts.panel import EdgeBandedPanel


EdgeBandedPanel(
    name='panel',
    length=800,
    width=200,
    thickness=18,
    material='plywood',
    front_edge_banding_thickness=10,
    back_edge_banding_thickness=10,
    left_edge_banding_thickness=10,
    right_edge_banding_thickness=10,
    edge_banding_style='length',
).run()
