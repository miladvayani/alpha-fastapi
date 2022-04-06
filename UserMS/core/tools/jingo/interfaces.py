from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from functools import wraps
import json
from typing import Optional
from faker.providers import BaseProvider

from json.encoder import JSONEncoder
from json.decoder import JSONDecoder

from .types import List
from .types import Callable
from .types import Any
from .types import ModuleType
from .types import Dict
from .types import overload
from .types import _T
from .types import Generic
from .types import Type

from .exceptions import ProviderError

from .base import Config
from .base import Faker
from .base import Generator


class JsonifierInterface(ABC):

    def __init__(self, 
            _json_module: ModuleType = json
        ) -> None:
        self.jsonify = _json_module
    
    @abstractmethod
    def _serializer(self, data: dict) -> str: ...

    @abstractmethod
    def _deserializer(self, data: str) -> dict: ...


class ModelInterface(ABC, Generic[_T]):

    config: Config = ...
    model: Type[_T] = ...
    
    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        self.providers: List[BaseProvider] = []
        self.__fields: List[Dict[str, FieldInterface]] = []
        self.execute_finding_fields()
        self.faker: Faker = Faker(**self.config)
        for provider in self.providers:
            self.faker.add_provider(provider)
        self.rendered_fields: List[Dict[str, Type[_T]]] = []
        self.execute_rendering_fields()
        self.jsonify_interface: JsonifierInterface = ...
        self.post_create_object(*args, **kwargs)
    
    @property
    def fields(self):
        return self.__fields

    @abstractmethod
    def execute_rendering_fields(self): pass

    @abstractmethod
    def execute_finding_fields(self): pass

    @abstractmethod
    def serializer(self) -> list[str]: pass

    @abstractmethod
    def deserailizer(self) -> list[dict]: pass

    def model_renderer(self, data: dict) -> Type[_T]:pass

    def post_create_object(self):
        pass
    
    def pre_create_object(self):
        pass

class FieldInterface(ABC):

    providers: List[BaseProvider] = ...

    def serialize_method(self) -> Any: return self.value 

    def deserialize_method(self) -> Any: return self.value 

    def __init__(self, 
            method: Callable, 
            default: Any = None,
            required: bool = True,
            visible: bool = True,
            randomable: bool = True,
            providers: Optional[BaseProvider] = None
        ) -> None:
        self.faker: Faker = ...
        self.method: Callable = method
        self.model: ModelInterface = ...
        self.required: bool = required
        self.visible: bool = visible
        self.randomable: bool = randomable
        self.default: Any = default
        self.value: Any = None
        if providers:
            self.providers.append(providers)

    def create_generator(self, model: ModelInterface):
        self.faker: Faker = model.faker
        self.model = model

    def create_field(self):
        return self.execute_method()

    def execute_method(self) -> Any:
        if not self.value:
            if self.method:
                self.value = self.method(self, self.faker)
            elif self.default is not None and self.method is None:
                self.value = self.default
        return self.value
