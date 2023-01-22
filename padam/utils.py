import csv
import io
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


def get_cutlist(part: Part, format='cutlistoptimizer'):
    if format == 'cutlistoptimizer':
        csv_file = io.StringIO()
        writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Length', 'Width', 'Qty', 'Material', 'Label', 'Enabled', 'Grain direction'])
        for panel in get_panel_list(part):
            writer.writerow([panel['length'], panel['width'], 1, panel['material'], panel['label'], 'true', 'v'])
        return csv_file.getvalue()
