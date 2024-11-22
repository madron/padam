import collections
from typing import Any, Dict, List, OrderedDict, Self
from pydantic import BaseModel, model_validator
from solid.solidpython import OpenSCADObject


class Part(BaseModel):
    name: str | None = None
    default: Dict[str, Any] = dict()
    parts: List[Self] | None = []

    @model_validator(mode='before')
    def default_values(cls, values: Any) -> Any:
        default = values.get('default', None)
        if default:
            fields = [x for x in list(cls.__pydantic_fields__.keys()) if x not in ('default', 'parts')]
            values_fields = list(values.keys())
            for field in fields:
                if field not in values_fields or values[field] is None:
                    value = default.get(field, None)
                    if value:
                        values[field] = value
        return values

    def __str__(self):
        return self.name or ''

    def add_part(self, part: Self) -> Self:
        self.parts.append(part)
        return part

    @property
    def materials(self):
        names = []
        if self.name:
            names.append(self.name)
        if self.parts:
            materials = []
            for part in self.parts:
                for material in part.materials:
                    material['names'] = names + material['names']
                    materials.append(material)
            return materials
        else:
            return [dict(names=names, part=self)]

    def get_object(self) -> OpenSCADObject:
        raise NotImplementedError()

    def get_objects(self) -> List[OpenSCADObject]:
        return [self.get_object()]

    def get_params(self) -> OrderedDict[str, Any]:
        return collections.OrderedDict([('name', self.name or '')])

    def run(self, **kwargs):
        from padam.command import run
        run(self, **kwargs)
