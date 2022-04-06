import string
from faker.providers import DynamicProvider
from faker.providers import BaseProvider
from faker.providers import address
from faker.providers import company
from faker.providers import color
from faker.providers import automotive
from faker.providers import bank
from faker.providers import barcode
from faker.providers import currency
from faker.providers import date_time
from faker.providers import credit_card
from faker.providers import person
from faker.providers import internet
from faker.providers import isbn
from faker.providers import file
from faker.providers import geo
from faker.providers import job
from faker.providers import profile
from faker.providers import python
from faker.providers import misc
from faker.providers import ssn
from faker.providers import lorem
from faker.providers import user_agent
from faker.providers import phone_number
from faker.generator import random
from faker.generator import mod_random
from faker.generator import Generator
from faker.typing import DateParseType
from faker.typing import GenderType
from faker.typing import HueType
from .types import Any
from .types import Optional
from .interfaces import ModelInterface
from bson.objectid import ObjectId


class Int32Provider(BaseProvider):

    def data(self, start=-2147483647, end=2147483647) -> int:
        return self.random_int(start, end)

class Int64Provider(BaseProvider):

    def data(self, start=-9223372036854775808, end=9223372036854775808) -> int:
        return self.random_int(start, end)
        
class FloatProvider(BaseProvider):

    def range(self, start=0, end=1) -> float:
        return random.uniform(start, end)

class BooleanProvider(BaseProvider):

    def bool(self, condition = True,randomable=False) -> bool:
        if randomable:
            return bool(round(random.random()))
        return condition

class EmbeddedProvider(BaseProvider):

    @staticmethod
    def __to_list(model: ModelInterface, counts: int):
        models: list[ModelInterface] = []
        for _ in range(counts):
            model_object:ModelInterface = model()
            models.append(model_object.from_model())
        return models

    @staticmethod
    def __to_dict(model: ModelInterface):
        return model().from_model()

    @staticmethod
    def import_to_model(model: ModelInterface, counts: int = 0) -> ModelInterface:
        if counts > 0:
            return EmbeddedProvider.__to_list(model, counts)
        return EmbeddedProvider.__to_dict(model)

class EnumProvider(BaseProvider):   

    def choice(self, choices: list) -> list:
        return random.choice(choices)

    def choices(self, population, weights=None, *, cum_weights=None, k=1) -> list:
        return random.choices(population, weights=weights, cum_weights=cum_weights, k=k)

class HashProvider(BaseProvider):

    def alphanumerical(self, length: int =16) -> str:
        data = "".join(self.random_elements(string.ascii_letters + string.digits, length=length))
        return data

class ObjectIdProvider(BaseProvider):
    
    def create(self) -> ObjectId:
        return ObjectId()

class RandomProvider(BaseProvider):

    pass    