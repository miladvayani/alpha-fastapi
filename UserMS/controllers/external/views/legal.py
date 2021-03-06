from fastapi import Request

from UserMS.core.contrib import CurrentUser
from UserMS.core.contrib import Response
from UserMS.core.contrib import validators
from UserMS.core.contrib import _
from UserMS.core.contrib import fields
from .. import router
from ..logic.legal import LegalRepository
from ..logic.user import UserRepository
from ..models.income.legal import *
from ..models.outcome.legal import *


@router.post("/legal/", response_model=AddLegalResponseModel)
async def add_legal(request: Request, legal: AddLegalIncomeModel):
    await validators.validate_province_city(legal.province_name, legal.city_name)
    current_user: CurrentUser = request.state.user
    user: dict = await UserRepository().get_user(user_id=current_user.id)
    repository: LegalRepository = LegalRepository()
    repository.check_user_info(user=user)
    repository.check_legal_duplicate_in_post(user["legal_info"], legal.buyer_id)
    result = await repository.add_legal(user_id=user["_id"], legal_data=legal.dict())
    return Response(data=result, detail=_("Legal info added successfully"))


@router.put("/legal/")
async def update_legal(request: Request, legal: UpdateLegalIncomeModel):
    await validators.validate_province_city(legal.province_name, legal.city_name)
    current_user: CurrentUser = request.state.user
    repository: LegalRepository = LegalRepository()
    user: dict = await UserRepository().get_user(user_id=current_user.id)
    repository.check_user_info(user=user)
    repository.check_legal_duplicate_in_update(
        user["legal_info"], new_buyer_id=legal.buyer_id, new_legal_id=legal.id
    )
    await repository.update_legal(
        user_id=current_user.id, legal_data=legal.dict(by_alias=True)
    )
    return Response(detail=_("Legal info updated successfully"))


@router.delete("/legal/{legal_id}")
async def delete_legal(request: Request, legal_id: fields.ObjectId):
    current_user: CurrentUser = request.state.user
    repository: LegalRepository = LegalRepository()
    user: dict = await UserRepository().get_user(user_id=current_user.id)
    repository.check_user_info(user=user)
    repository.check_is_used_legal_for_delete(
        exist_legal_info=user["legal_info"], legal_id=legal_id
    )
    await repository.delete_legal(user_id=current_user.id, legal_id=legal_id)
    return Response(detail=_("Legal info deleted successfully"))
