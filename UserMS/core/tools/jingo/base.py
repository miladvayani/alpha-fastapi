from __future__ import annotations
import json

from .types import Generic
from .types import _T
from .types import overload
from .types import List
from .types import Optional
from .types import Dict
from .types import Any
from .types import Type
from .types import _KT
from .types import _VT
from .types import Union
from .types import Sequence
from .types import ModuleType

from faker import Faker
from faker import Generator
from faker import Factory

from .exceptions import ConfigKeyType
from .exceptions import ConfigValueType


class Options(Generic[_T]):

    def __init__(self, **kwargs: Type[_T]) -> None:
        self.options: Type[_T] = kwargs

    def export(self) -> Type[_T]:
        return self.options


class Config(dict):
    
    @overload
    def __init__(self, strict_mode: bool) -> None:
        """
            Config will need to add key values
        """

    @overload
    def __init__(self, properties: Optional[Properties] = None, *, strict_mode: bool) -> None:
        """
            Config will catch the data from `Properties`
        """

    def __init__(self, properties: Optional[Properties] = None, strict_mode: bool = True) -> None:
        self.strict_mode: bool = strict_mode
        if properties:
            for key, value in properties.decompose().items():
                self.__setitem__(key, value)
        super().__init__()

    def __getitem__(self, __k: _KT) -> _VT:
        if isinstance(__k , str):
            return super().__getitem__(__k)
        raise ConfigKeyType(
            __k
            ) from Exception

    def __setitem__(self, __k: _KT, v: _VT) -> None:
        if self.strict_mode:
            if isinstance(v, (
                    str,
                    int,
                    tuple,
                    dict,
                    list,
                    set,
                    float,
                    )
                ) or v is None:
                pass
            else:    
                raise ConfigValueType(v)
        return super().__setitem__(__k, v)

class Properties(object):

    def __init__(self, 
            locale: Union[str, Sequence[str] , Dict[str, int , float] , None] = None, 
            providers: Union[List[str] , None] = None, 
            generator: Union[Generator , None] = None, 
            includes: Union[List[str] , None] = None, 
            use_weighting: bool = True, 
            randomize: bool = True, 
            jsonifier: ModuleType = json,
            **config: Any
        ) -> None:
        self.locale = locale
        self.providers = providers
        self.generator = generator
        self.includes = includes
        self.use_weighting = use_weighting
        self.config = config
        self.randomize = randomize
        self.jsonifier = jsonifier
        self.configure(config)

    def configure(self, config: dict):
        for key, value in config.items():
            setattr(self, key, value)

    def decompose(self) -> dict:
        return self.__dict__

    @staticmethod
    def reconfigure(object_: Properties, properties: Properties) -> Properties:
        properties_ = {}
        properties_.update(object_.decompose())
        properties_.update(properties.decompose())
        return Properties(**properties_)
