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
        """check user buyer id existence either commited or not.
        if not added personal information should raise error and
        the user has to complete its own inforamtion due to the profile.

        Args:
            user (dict): user info

        Raises:
            HTTPException: Please complete your personal info , Bad Request(404)
        """
        if user["buyer_id"] is None:
            raise HTTPException(
                400, detail=_("Please complete your personal information first")
            )

    def check_legal_duplicate_in_post(
        self, exist_legal_info: List[dict], new_buyer_id: str
    ):
        """check income legal data to find dubplicate info if new buyer id
        already exists for the found user.

        Args:
            exist_legal_info (List[dict]): list of legal info that retrieved from database.
            new_buyer_id (str): new buyer id

        Raises:
            HTTPException: if there was duplicate buyer id in `exist_legal_info will` ``raise``
            'Legal info already exists'.
        """
        for legal in exist_legal_info:
            if legal["buyer_id"] == new_buyer_id:
                raise HTTPException(400, _("Legal info already exists"))

    async def add_legal(self, user_id: str, legal_data: dict) -> dict:
        """add new legal info to the user

        Args:
            user_id (str): targer user
            legal_data (dict): new lagal data

        Returns:
            dict: inseted id of new legal
        """
        inserted_id = await self.layer.add_legal_for_user(
            user_id=ObjectId(user_id), legal_data=legal_data
        )
        return {"_id": inserted_id}

    def check_legal_duplicate_in_update(
        self, exist_legal_info: List[dict], new_buyer_id: str, new_legal_id: ObjectId
    ) -> None:
        """check duplicate legal info in the user document in terms of buyer id and legal id
        if legal id is matched with retrieved legal from user will update without any concern
        otherwise will raise 404 and also will check the usage of legal whole the system if
        this applied as used would also raise 400.

        Args:
            exist_legal_info (List[dict]): list of retrieved legal info from user
            new_buyer_id (str): new buyer id
            new_legal_id (ObjectId): new legal id

        Raises:
            HTTPException: if is used `True` will raise 400 'Legal info in use'
            HTTPException: if new buyer id already exists will raise 400 'Legal info already exists'
            HTTPException: else will raise 404 'not found'
        """
        found = False
        for legal in exist_legal_info:
            if legal["_id"] == new_legal_id:
                if legal["is_used"]:
                    raise HTTPException(400, _("Legal info in use"))
                else:
                    found = True
            elif legal["buyer_id"] == new_buyer_id:
                raise HTTPException(400, _("Legal info already exists"))
        if not found:
            raise HTTPException(404, _("Legal info not found"))

    async def update_legal(self, user_id: str, legal_data: dict) -> None:
        """update legal info

        Args:
            user_id (str): targer user id
            legal_data (dict): new legal data
        """
        await self.layer.update_legal_of_user(
            user_id=ObjectId(user_id), legal_data=legal_data
        )

    def check_is_used_legal_for_delete(
        self, exist_legal_info: List[dict], legal_id: ObjectId
    ) -> None:
        """if legal id is matched with retrieved legal from user will update without any concern
        otherwise will raise 404 and also will check the usage of legal whole the system if
        this applied as used would also raise 400.

        Args:
            exist_legal_info (List[dict]): list of retrieved legal info from user
            legal_id (ObjectId): targer legal

        Raises:
            HTTPException: if is used `True` will raise 400 'Legal info in use'
            HTTPException: else will raise 404 'not found'
        """
        found = False
        for legal in exist_legal_info:
            if legal["_id"] == legal_id:
                if legal["is_used"]:
                    raise HTTPException(400, _("Legal info in use"))
                found = True
                break
        if not found:
            raise HTTPException(404, _("Legal info not found"))

    async def delete_legal(self, user_id: str, legal_id: ObjectId) -> None:
        """delete legal info

        Args:
            user_id (str): targer user
            legal_id (ObjectId): targer legal
        """
        await self.layer.delete_legal_of_user(
            user_id=ObjectId(user_id), legal_id=legal_id
        )
