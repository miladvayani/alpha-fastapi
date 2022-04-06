from typing import List
from UserMS.data.creator import DataLayer
from UserMS.data.creator import MongoDataLayer
from UserMS.core.i18n import _
from bson.objectid import ObjectId
from fastapi import HTTPException


class LegalRepository:
    def __init__(self) -> None:
        self.layer = DataLayer[MongoDataLayer]("mongo").create_user_data_layer()

    def check_user_info(self, user: dict) -> None:
        if user["buyer_id"] is None:
            raise HTTPException(
                400, detail=_("Please complete your personal information first")
            )

    def check_legal_duplicate_in_post(
        self, exist_legal_info: List[dict], new_buyer_id: str
    ):
        for legal in exist_legal_info:
            if legal["buyer_id"] == new_buyer_id:
                raise HTTPException(400, _("Legal info already exists"))

    async def add_legal(self, user_id: str, legal_data: dict) -> dict:
        inserted_id = await self.layer.add_legal_for_user(
            user_id=ObjectId(user_id), legal_data=legal_data
        )
        return {"_id": inserted_id}

    def check_legal_duplicate_in_update(
        self, exist_legal_info: List[dict], new_buyer_id: str, new_legal_id: ObjectId
    ) -> None:
        found = False
        for legal in exist_legal_info:
            if legal["_id"] == new_legal_id:
                if legal["is_used"]:
                    raise HTTPException(400, _("Legal info in use"))
                else:
                    found = True
            elif legal["buyer_id"] == new_buyer_id:
                print("hello")
                raise HTTPException(400, _("Legal info already exists"))
        if not found:
            raise HTTPException(404, _("Legal info not found"))

    async def update_legal(self, user_id: str, legal_data: dict) -> None:
        await self.layer.update_legal_of_user(
            user_id=ObjectId(user_id), legal_data=legal_data
        )

    def check_is_used_legal_for_delete(
        self, exist_legal_info: List[dict], legal_id: ObjectId
    ) -> None:
        found = False
        for legal in exist_legal_info:
            if legal["_id"] == legal_id:
                if legal["is_used"]:
                    raise HTTPException(400, _("Legal info in use"))
        if not found:
            raise HTTPException(404, _("Legal info not found"))

    async def delete_legal(self, user_id: str, legal_id: ObjectId) -> bool:
        await self.layer.delete_legal_of_user(
            user_id=ObjectId(user_id), legal_id=legal_id
        )
