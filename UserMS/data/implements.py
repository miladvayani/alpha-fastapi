from __future__ import annotations
from pprint import pprint
from typing import List, Tuple, Union
from .interfaces import UserDataLayer
from .interfaces import DataLayerInterface
from .interfaces import T
from bson.objectid import ObjectId
from pymongo.results import UpdateResult
from .. import Application as root
from .entity import User, LegalInfo
from pymongo.results import InsertOneResult
from pymongo.results import UpdateResult
from UserMS.core.hydantic.options import create_unset_optional_model


class MongoDataLayer(DataLayerInterface):
    def create_user_data_layer(self) -> MongoUserDataLayer:
        return MongoUserDataLayer()


class MongoUserDataLayer(UserDataLayer):
    model: User = User

    def to_model(self, data: dict) -> T:
        return self.model(**data)

    async def get_current_user(self, user_id: Union[ObjectId, str]) -> dict:
        return await root.db[self.collection].find_one({"_id": ObjectId(user_id)})

    async def get_user_by_mobile(self, mobile: str) -> dict:
        return await root.db[self.collection].find_one({"mobile_number": mobile})

    async def insert_user(self, data: dict) -> dict:
        document: User = self.to_model(data)
        result: InsertOneResult = await root.db[self.collection].insert_one(
            document=document.dict(by_alias=True)
        )
        document.id = result.inserted_id
        return document.dict(by_alias=True)

    async def update_user(
        self, user_id: Union[ObjectId, str], document: dict
    ) -> List[ObjectId, int]:
        user = create_unset_optional_model(User, document)
        print(user)
        result: UpdateResult = await root.db[self.collection].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": user},
        )
        return [result.upserted_id, result.matched_count]

    async def update_bulk_user(self, query: dict, document: dict) -> UpdateResult:
        result: UpdateResult = await root.db[self.collection].update_many(
            query,
            {"$set": create_unset_optional_model(User, document)},
        )
        return result

    async def add_legal_for_user(self, user_id: ObjectId, legal_data: dict) -> ObjectId:
        legal = LegalInfo(**legal_data)
        await root.db[self.collection].update_one(
            {"_id": user_id}, {"$push": {"legal_info": legal.dict(by_alias=True)}}
        )
        return legal.id

    async def get_bulk_users(self, query: dict) -> List[dict]:
        documents: List[dict] = []
        result: List[dict] = await root.db[self.collection].find(query)
        async for document in result:
            documents.append(document)
        return documents

    async def update_legal_of_user(self, user_id: ObjectId, legal_data: dict) -> None:
        legal = LegalInfo(**legal_data)
        await root.db[self.collection].update_one(
            {"_id": user_id, "legal_info._id": legal.id},
            {"$set": {"legal_info.$": legal.dict(by_alias=True)}},
        )

    async def delete_legal_of_user(self, user_id: ObjectId, legal_id: ObjectId) -> None:
        await root.db[self.collection].update_one(
            {"_id": user_id}, {"$pull": {"legal_info": {"_id": legal_id}}}
        )
