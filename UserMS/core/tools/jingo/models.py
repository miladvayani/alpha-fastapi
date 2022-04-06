from inspect import isclass
from typing import Generic
from faker.providers import BaseProvider

from .types import Type
from .types import Any
from .types import _T
from .types import Dict
from .types import List
from .types import Optional
from .interfaces import ModelInterface
from .interfaces import FieldInterface
from .interfaces import JsonifierInterface
from .providers import random
from copy import deepcopy


class BaseFakeModel(ModelInterface):
    def execute_finding_fields(self):
        self.__find_fields()
        self.__find_providers()

    def execute_rendering_fields(self):
        self.__field_rendering()

    def from_model(self) -> Type[_T]:
        return self.__import_to_model()

    def serializer(
        self,
        exclude: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        unknown: Optional[Dict] = {},
    ) -> list[str]:
        jsonifier: JsonifierInterface = self.config["jsonifier"]
        fields_value: List[Dict[str, FieldInterface]] = []
        for field in self.fields:
            row: dict = {}
            for key, field_object in field.items():
                if exclude:
                    if key not in exclude:
                        row[key] = field_object.serialize_method()
                if include:
                    if key in include:
                        row[key] = field_object.serialize_method()
        row.update(unknown)
        fields_value.append(row)
        result: list[str] = [jsonifier._serializer(data) for data in fields_value]
        return result

    def deserailizer(
        self,
        exclude: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        unknown: Optional[Dict] = {},
    ) -> list[dict]:
        jsonifier: JsonifierInterface = self.config["jsonifier"]
        fields_value: List[Dict[str, FieldInterface]] = []
        for field in self.fields:
            row: dict = {}
            for key, field_object in field.items():
                if exclude:
                    if key not in exclude:
                        row[key] = field_object.deserialize_method()
                elif include:
                    if key in include:
                        row[key] = field_object.deserialize_method()
                else:
                    row[key] = field_object.deserialize_method()
        row.update(unknown)
        fields_value.append(row)
        result: list[dict] = [jsonifier._deserializer(data) for data in fields_value]
        return result

    def __find_fields(self):
        fields = dict(self.__class__.__base__.__dict__.items()) | dict(
            self.__class__.__dict__.items()
        )
        self.fields.append(
            {
                key: field
                for key, field in fields.items()
                if isinstance(field, FieldInterface)
            }
        )

    def __find_providers(self):
        for item in self.fields:
            for key, field in item.items():
                for provider in field.providers:
                    if isclass(provider):
                        if issubclass(provider, BaseProvider):
                            if provider not in self.providers:
                                self.providers.append(provider)

    def __field_rendering(self):
        for item in self.fields:
            for key, field in item.items():
                field.create_generator(self)
                required = field.required
                visibile = field.visible
                if field.model.config["randomize"]:
                    if field.randomable:
                        required = bool(round(random.randint(0, 1)))
                        visibile = bool(round(random.randint(0, 1)))
                else:
                    pass
                self.__render(key, field, required=required, visibile=visibile)

    def __render(self, key: str, field: FieldInterface, required: bool, visibile: bool):
        result = None
        field.value = None
        if visibile:
            if required:
                result = field.create_field()
            self.rendered_fields.append({key: result})

    def change_value(self, __k: str, __v: Any):
        for item in self.fields:
            finded_field = item[__k]
            finded_field.value = __v
            for rf in self.rendered_fields:
                rf[__k] = __v

    def __repr__(self) -> str:
        context: str = ...
        kw: list = []
        for field in self.rendered_fields:
            for key, value in field.items():
                kw.append(f"{key}={value}")
        context = f"{self.__class__.__name__}({','.join(kw)})"
        context += ")"
        return context

    def __import_to_model(self) -> Type[_T]:
        data: dict = dict()
        if self.model:
            for item in self.rendered_fields:
                for key, value in item.items():
                    data[key] = value
        model = self.model_renderer(data)
        return model
