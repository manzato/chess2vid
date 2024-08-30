from chess import WHITE, Color

_light_material = None

_dark_material = None


def set_light_material(material):
    global _light_material
    _light_material = material


def get_light_material():
    global _light_material
    return _light_material


def set_dark_material(material):
    global _dark_material
    _dark_material = material


def get_dark_material():
    global _dark_material
    return _dark_material


def apply_material(color: Color, object):
    material = get_light_material() if color == WHITE else get_dark_material()
    object.data.materials.append(material)
