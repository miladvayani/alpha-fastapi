from abc import ABC
from abc import abstractmethod
from abc import abstractstaticmethod
import json
from typing import Any, Generic, Tuple
from typing import TypeVar
from bson.objectid import ObjectId
from pydantic import BaseModel


T = TypeVar("T", BaseModel, object)


class DataLayerInterface(ABC):
    @abstractmethod
    def create_user_data_layer(self) -> ...:
        ...


class UserDataLayer(Generic[T], ABC):

    model: T
    json_interface: json

    @property
    def collection(self) -> str:
        return self.model.__name__.lower()

    @abstractmethod
    async def get_current_user(self, user_id: ObjectId) -> dict:
        ...

    @abstractmethod
    async def insert_user(self, data: dict) -> None:
        ...

    @abstractmethod
    async def update_user(self, query: dict, set: dict) -> None:
        ...

    @abstractmethod
    def to_model(self, data: dict) -> T:
        ...

    @abstractmethod
    async def add_legal_for_user(self, user_id: ObjectId, legal_data: dict) -> ObjectId:
        ...

    @abstractmethod
    async def update_legal_of_user(self, user_id: ObjectId, legal_data: dict) -> None:
        ...

    @abstractmethod
    async def delete_legal_of_user(self, user_id: ObjectId, legal_id: ObjectId) -> None:
        ...
