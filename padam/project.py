from copy import copy
from typing import Any, Dict
from pydantic import BaseModel
from pydantic import BaseModel, Field, field_validator


class Project(BaseModel):
    default: Dict[str, Dict[str, Any]] | None = dict()

    @field_validator('default')
    @classmethod
    def get_default(cls, data: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        return get_default(data)


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
