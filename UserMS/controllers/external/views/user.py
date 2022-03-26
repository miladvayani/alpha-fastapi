from fastapi import Request

from UserMS import CurrentUser
from UserMS.core.i18n import _
from UserMS import ResponseObject as Response
from .. import router

from ..logic.user import *
from ..models.income.user import *
from ..models.outcome.user import *


@router.get(
    "/user/",
    response_model=UserResponse,
)
async def get_user(request: Request):
    current_user: CurrentUser = request.state.user
    repository: UserRepository = UserRepository()
    user: dict = await repository.get_user(user_id=current_user.id)
    return Response(data=user)


@router.put("/user/")
async def update_user(request: Request, data: UserUpdateIncomeModel):
    current_user: CurrentUser = request.state.user
    repository: UserRepository = UserRepository()
    user: dict = await repository.get_user(user_id=current_user.id)
    await repository.update_user(user=user, data=data)
    return Response(detail=_("Your info updated successfully"))
