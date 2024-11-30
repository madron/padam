CUTLIST_FORMATS = ['cutlistoptimizer']
CUTLIST_DEFAULT_FORMAT = 'cutlistoptimizer'

MATERIAL_COLOR = dict(
    plywood='#f8f2dc',
    hardwood='#cba791',
)

for key, value in MATERIAL_COLOR.items():
    if isinstance(value, str):
        hex_string = value.lstrip('#')
        color = [int(hex_string[i:i+2], 16) / 256 for i in (0, 2, 4)]
        MATERIAL_COLOR[key] = color
