from UserMS.data.creator import DataLayer
from UserMS.data.creator import MongoDataLayer
from UserMS.core.contrib import _
from bson.objectid import ObjectId
from fastapi import HTTPException


class UserRepository:
    def __init__(self) -> None:
        self.layer = DataLayer[MongoDataLayer]("mongo").create_user_data_layer()

    async def get_user(self, user_id: ObjectId) -> dict:
        """ger current user

        Args:
            user_id (ObjectId): user id

        Raises:
            HTTPException: if not found will raise 404

        Returns:
            dict: retrieved user
        """
        user = await self.layer.get_current_user(user_id=user_id)
        if user:
            return user
        raise HTTPException(404, _("No Such User Exists"))

    async def update_user(self, user: dict, data: dict) -> None:
        """update user

        Args:
            user (dict): retrieved user
            data (dict): new data for user from income model
        """
        for key, value in data.items():
            user[key] = value
        await self.layer.update_user(user_id=user["_id"], document=user)
