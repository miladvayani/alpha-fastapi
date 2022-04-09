from typing import List
from UserMS.core.hydantic.fields import ObjectId
from UserMS.data.creator import DataLayer
from UserMS.data.creator import MongoDataLayer
from UserMS.core.contrib import RabbitException
from UserMS.core.contrib import Status


class UserRepository:
    def __init__(self) -> None:
        self.layer = DataLayer[MongoDataLayer]("mongo").create_user_data_layer()

    async def get_user_by_id(self, user_id: str) -> dict:
        """get user by id

        Args:
            user_id (str): target user

        Raises:
            RabbitException: if not found will raise error and nack

        Returns:
            dict: retrieved user
        """
        user = await self.layer.get_current_user(user_id=user_id)
        if user:
            return user
        raise RabbitException(Status.nack, "No Such User Exists")

    async def get_users(self, query: dict) -> List[dict]:
        """get users

        Args:
            query (dict): query

        Returns:
            List[dict]: list of users
        """
        users: List[dict] = self.layer.get_bulk_users(query)
        return users

    async def set_user_by_mobile(self, mobile_number: str) -> ObjectId:
        """set new user but at the first step checks that whether user exists or not
        if user exists will return the user id otherwise will add new user then return
        inserted id

        Args:
            mobile_number (str): mobile number to search user

        Returns:
            ObjectId: user id
        """
        user: dict = await self.layer.get_user_by_mobile(mobile_number)
        if user:
            return user["_id"]
        new_user_id = await self.layer.insert_user(dict(mobile_number=mobile_number))
        return new_user_id

    async def update_one_user(self, user_id: str, new_data: dict) -> bool:
        """update user

        Args:
            user_id (str): target user id
            new_data (dict): new user data

        Returns:
            bool: update status
        """
        upserted_id, matched_count = await self.layer.update_user(
            user_id=user_id, document=new_data
        )
        if upserted_id or matched_count > 0:
            return True
        return False

    async def update_bulk_user(self, query: dict, new_data: dict) -> int:
        """update many users

        Args:
            query (dict): query
            new_data (dict): new data

        Returns:
            int: updated count
        """
        result = await self.layer.update_bulk_user(query=query, document=new_data)
        return result.modified_count
