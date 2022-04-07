from typing import List
from UserMS.data.creator import DataLayer
from UserMS.data.creator import MongoDataLayer
from UserMS.core.contrib import RabbitException
from UserMS.core.contrib import Status


class UserRepository:
    def __init__(self) -> None:
        self.layer = DataLayer[MongoDataLayer]("mongo").create_user_data_layer()

    async def get_user_by_id(self, user_id: str) -> dict:
        user = await self.layer.get_current_user(user_id=user_id)
        if user:
            return user
        raise RabbitException(Status.nack, "No Such User Exists")

    async def get_users(self, query: dict) -> List[dict]:
        users: List[dict] = self.layer.get_bulk_users(query)
        return users

    async def set_user_by_mobile(self, mobile_number: str) -> dict:
        user: dict = await self.layer.get_user_by_mobile(mobile_number)
        if user:
            return user["_id"]
        new_user_id = await self.layer.insert_user(dict(mobile_number=mobile_number))
        return new_user_id

    async def update_one_user(self, user_id: str, new_data: dict) -> bool:
        upserted_id, matched_count = await self.layer.update_user(
            user_id=user_id, document=new_data
        )
        if upserted_id or matched_count > 0:
            return True
        return False

    async def update_bulk_user(self, query, new_data: dict) -> int:
        result = await self.layer.update_bulk_user(query=query, document=new_data)
        if result.modified_count > 0 and result.modified_count == 0:
            return result.modified_count
        return 0
