import re
from copy import copy
from typing import Any, Dict, Type
from pydantic import BaseModel
from pydantic import BaseModel, field_validator
from padam import parts


class Project(BaseModel):
    parameter: Dict[str, Any] | None = dict()
    default: Dict[str, Dict[str, Any]] | None = dict()
    part: Dict[str, Any] | None = dict()

    @field_validator('parameter')
    @classmethod
    def get_parameter(cls, data: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        return get_parameter(data)

    @field_validator('default')
    @classmethod
    def get_default(cls, data: Dict[str, Dict[str, Any]], values: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        return get_default(data, parameter=values.data.get('parameter', dict()))

    @field_validator('part')
    @classmethod
    def get_part(cls, data: Dict[str, Any], values: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        return get_part(data, default=values.data.get('default', dict()), parameter=values.data.get('parameter', dict()))

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


def get_parameter(data: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, Any]]:
    parameter = dict()
    for k, v in data.items():
        value = v
        if isinstance(value, str):
            for pk, pv in parameter.items():
                value = re.sub(r"\b{}\b".format(pk), str(pv), value)
            try:
                value = eval(value)
            except NameError as e:
                raise ValueError("error in '{}': {}".format(k, str(e)))
        parameter[k] = value
    return parameter


def get_default(data: Dict[str, Dict[str, Any]], parameter: Dict[str, Any] | None = dict()) -> Dict[str, Dict[str, Any]]:
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
        section_value_copy = dict()
        for k, v in section_value.items():
            value = v
            for pk, pv in parameter.items():
                value = re.sub(r"\b{}\b".format(pk), str(pv), str(value))
            if not value == v:
                value = eval(value)
            section_value_copy[k] = value
        default[section_name].update(section_value_copy)
    if has_parent(default):
        default = get_default(default)
    return default


def get_part(data: Dict[str, Any], default: Dict[str, Dict[str, Any]], parameter: Dict[str, Any] | None = dict()) -> Dict[str, Any]:
    result = dict()
    for part_name, part_value in data.items():
        default_value = dict()
        if 'default' in part_value:
            default_name = part_value.pop('default')
            default_value = default.get(default_name, dict())
        part_class = get_part_class(part_value['type'])
        for k, v in part_value.items():
            value = v
            for pk, pv in parameter.items():
                value = re.sub(r"\b{}\b".format(pk), str(pv), str(value))
            if not value == v:
                value = eval(value)
            part_value[k] = value
        result[part_name] = part_class(name=part_name, default=default_value, **part_value)
    return result


def get_part_class(name: str) -> Type[parts.Part]:
    class_dict = dict(
        cabinet=parts.Cabinet,
        frame=parts.Frame,
        edgebandedpanel=parts.Panel,
        basepanel=parts.BasePanel,
        panel=parts.Panel,
    )
    return class_dict[name]
