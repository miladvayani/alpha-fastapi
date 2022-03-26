from __future__ import annotations
from typing import Tuple, Union
from .interfaces import UserDataLayer
from .interfaces import DataLayerInterface
from .interfaces import T
from bson.objectid import ObjectId
from pymongo.results import UpdateResult
from .. import Application as root
from .entity import User, LegalInfo
from pymongo.results import InsertOneResult
from pymongo.results import UpdateResult


class MongoDataLayer(DataLayerInterface):
    def create_user_data_layer(self) -> MongoUserDataLayer:
        return MongoUserDataLayer()


class MongoUserDataLayer(UserDataLayer):
    model: User = User

    def to_model(self, data: dict) -> T:
        return self.model(**data)

    async def get_current_user(self, user_id: Union[ObjectId, str]) -> dict:
        return await root.db[self.collection].find_one({"_id": ObjectId(user_id)})

    async def insert_user(self, data: dict) -> None:
        await root.db[self.collection].insert_one(self.to_model(data).dict())

    async def update_user(self, user_id: Union[ObjectId, str], document: dict) -> None:
        await root.db[self.collection].update_one(
            {"_id": ObjectId(user_id)}, {"$set": document}
        )

    async def add_legal_for_user(self, user_id: ObjectId, legal_data: dict) -> ObjectId:
        legal = LegalInfo(legal_data)
        await root.db[self.collection].update_one(
            {"_id": user_id}, {"$push": {"legal_info": legal.dict(by_alias=True)}}
        )
        return legal.id

    async def update_legal_of_user(self, user_id: ObjectId, legal_data: dict) -> None:
        legal = LegalInfo(legal_data)
        await root.db[self.collection].update_one(
            {"_id": user_id, "legal_info._id": legal.id},
            {"$set": {"legal_info.$": legal.dict(by_alias=True)}},
        )

    async def delete_legal_of_user(self, user_id: ObjectId, legal_id: ObjectId) -> None:
        await root.db[self.collection].update_one(
            {"_id": user_id}, {"$pull": {"legal_info": {"_id": legal_id}}}
        )
