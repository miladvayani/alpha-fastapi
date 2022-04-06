from bson.objectid import ObjectId
from .types import Any

from .interfaces import FieldInterface, ModelInterface

from .providers import BooleanProvider
from .providers import FloatProvider
from .providers import HashProvider
from .providers import ObjectIdProvider
from .providers import address
from .providers import company
from .providers import barcode
from .providers import currency
from .providers import date_time
from .providers import person
from .providers import job
from .providers import lorem
from .providers import phone_number
from .providers import Int32Provider
from .providers import Int64Provider
from .providers import EmbeddedProvider
from .providers import RandomProvider
from .providers import EnumProvider


class TextField(FieldInterface):

    providers: list = [
        lorem,
        ]


class HashField(FieldInterface):

    native_provider: bool = False

    providers: list = [
        HashProvider
    ]


class StrField(FieldInterface):

    providers: list = [
        person,
        job,
        address,
        phone_number,
        company,
        barcode,
        currency
    ]


class EnumField(FieldInterface):

    providers: list = [ 
        EnumProvider
    ]


class Int32Field(FieldInterface):

    providers: list = [
        Int32Provider
    ]

class Int64Field(FieldInterface):

    providers: list = [
        Int64Provider
    ]

class FloatField(FieldInterface):

    providers: list = [
        FloatProvider
    ]


class BooleanField(FieldInterface):

    providers: list = [
        BooleanProvider
    ]


class ListField(FieldInterface):

    providers: list = [ 
        EmbeddedProvider
    ]

    def __init__(self,
            observer: ModelInterface,
            counts: int = 1,
            *args, 
            **kwargs
        ) -> None:
        super().__init__(self.__import_from_embedded_model, *args, **kwargs)
        self.observer: ModelInterface = observer
        if counts < 1:
            self.counts = 1
        else:
            self.counts: int = counts

    def execute_method(self) -> Any:
        self.value = self.method(EmbeddedProvider)    
        return self.value

    def __import_from_embedded_model(self, provider: EmbeddedProvider):
        return provider.import_to_model(self.observer, self.counts)


class KVField(FieldInterface):

    providers: list = [ 
        EmbeddedProvider
    ]

    def __init__(self,
            observer: ModelInterface,
            *args, 
            **kwargs
        ) -> None:
        super().__init__(self.__import_from_embedded_model, *args, **kwargs)
        self.observer: ModelInterface = observer

    def execute_method(self) -> Any:
        self.value = self.method(EmbeddedProvider)    
        return self.value

    def __import_from_embedded_model(self, provider: EmbeddedProvider):
        return provider.import_to_model(self.observer, 0)
    

class TupleField(FieldInterface):

    pass

class SetField(FieldInterface):

    pass


class DateTimeField(FieldInterface):

    providers: list = [ 
        date_time
    ]
    
    def serialize_method(self) -> Any:
        return str(self.value)

    def deserialize_method(self) -> Any:
        return str(self.value)
        
class RandomField(FieldInterface):

    providers: list = [ 
        RandomProvider,
    ]

class ObjectField(FieldInterface):

    native_provider: bool = False

    providers: list = [ 
        ObjectIdProvider
    ]

    def serialize_method(self) -> None:
        return str(ObjectId(self.value))

    def deserialize_method(self) -> None:
        try:
            return str(ObjectId(self.value))
        except TypeError:
            raise TypeError(self.value)