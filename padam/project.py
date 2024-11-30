from copy import copy
from typing import Any, Dict, Type
from pydantic import BaseModel
from pydantic import BaseModel, field_validator
from padam import parts


class Project(BaseModel):
    default: Dict[str, Dict[str, Any]] | None = dict()
    part: Dict[str, Any] | None = dict()

    @field_validator('default')
    @classmethod
    def get_default(cls, data: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        return get_default(data)

    @field_validator('part')
    @classmethod
    def get_part(cls, data: Dict[str, Any], values: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        return get_part(data, values.data['default'])

    def get_objects(self):
        objs = list()
        for part in self.part.values():
            objs.extend(part.get_objects())
        return objs

    def get_materials(self):
        names = []
        materials = []
        for part in self.part.values():
            for material in part.get_materials():
                material['names'] = names + material['names']
                materials.append(material)
        return materials


def has_parent(data: Dict[str, Dict[str, Any]]) -> bool:
    for section_value in data.values():
        if 'inherits' in section_value:
            return True
    return False


def get_default(data: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    default = dict()
    for section_name, section_value in data.items():
        if 'inherits' in section_value:
            try:
                parent = data[section_value['inherits']]
            except KeyError:
                raise ValueError('section "{}" inherits from non existent section "{}"'.format(section_name, section_value['inherits']))
            default[section_name] = copy(parent)
            del section_value['inherits']
        else:
            default[section_name] = dict()
        default[section_name].update(section_value)
    if has_parent(default):
        default = get_default(default)
    return default


def get_part(data: Dict[str, Any], default: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    result = dict()
    for part_name, part_value in data.items():
        default_value = dict()
        if 'default' in part_value:
            default_name = part_value.pop('default')
            default_value = default[default_name]
        part_class = get_part_class(part_value['type'])
        result[part_name] = part_class(name=part_name, default=default_value, **part_value)
    return result


def get_part_class(name: str) -> Type[parts.Part]:
    class_dict = dict(
        cabinet=parts.Cabinet,
        frame=parts.Frame,
        edgebandedpanel=parts.EdgeBandedPanel,
        panel=parts.Panel,
    )
    return class_dict[name]
