from UserMS.data.creator import DataLayer
from UserMS.data.creator import MongoDataLayer
from UserMS.core.contrib import _
from UserMS.core.contrib import validators
from UserMS import Application as root
from bson.objectid import ObjectId
from fastapi import HTTPException
from ..models.income.user import UserUpdateIncomeModel


class UserRepository:
    def __init__(self) -> None:
        self.layer = DataLayer[MongoDataLayer]("mongo").create_user_data_layer()

    async def get_user(self, user_id: ObjectId) -> dict:
        user = await self.layer.get_current_user(user_id=user_id)
        if user:
            return user
        raise HTTPException(404, _("No Such User Exists"))

    async def update_user(self, user: dict, data: dict) -> None:
        await validators.validate_job(root.config["MONGO_DB"], job=data["job"])
        for key, value in data.items():
            user[key] = value
        await self.layer.update_user(user_id=user["_id"], document=user)
