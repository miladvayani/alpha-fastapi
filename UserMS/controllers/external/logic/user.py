from UserMS.data.creator import DataLayer
from UserMS.data.creator import MongoDataLayer
from UserMS.core.i18n import _
from UserMS import Application as root
from bson.objectid import ObjectId
from fastapi import HTTPException
import requests
from ..models.income.user import UserUpdateIncomeModel


class UserRepository:
    def __init__(self) -> None:
        self.layer = DataLayer[MongoDataLayer]("mongo").create_user_data_layer()

    async def get_user(self, user_id: ObjectId) -> dict:
        user = await self.layer.get_current_user(user_id=user_id)
        if user:
            return user
        raise HTTPException(404, _("No Such User Exists"))

    async def validate_job(self, job: str) -> None:
        resp = requests.get(root.config["CONSTANTS_MS_URL"] + "validate_job/" + job)
        if resp.status_code != 200:
            raise HTTPException(400, detail=_("Selected Job is Invalid"))

    async def update_user(self, user: dict, data: UserUpdateIncomeModel) -> None:

        document: dict = data.dict()
        await self.validate_job(job=data.job)
        for key, value in document.items():
            user[key] = value
        await self.layer.update_user(user_id=user["_id"], document=user)
