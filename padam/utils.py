from padam.parts import Part
from padam.parts.panel import Panel


def get_panel_list(part: Part):
    panels = []
    materials = part.materials
    for panel in [m for m in materials if isinstance(m, Panel)]:
        if panel.material:
            material_label = '{}_{}'.format(panel.material, panel.thickness)
        else:
            material_label = str(panel.thickness)
        panels.append(
            dict(
                label=panel.name,
                material=material_label,
                length=panel.length,
                width=panel.width,
            )
        )
    return panels
