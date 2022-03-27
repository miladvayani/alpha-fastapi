from fastapi import Request
from aio_pika import Message

from UserMS import CurrentUser
from UserMS import Application as root
from UserMS.core.i18n import _
from UserMS import ResponseObject as Response
from UserMS.core.rabbit import RabbitCall
from .. import router

from ..logic.user import *
from ..models.income.user import *
from ..models.outcome.user import *


@router.get(
    "/user/",
    tags=["Users"],
    response_model=UserResponse,
)
async def get_user(request: Request):
    current_user: CurrentUser = request.state.user
    repository: UserRepository = UserRepository()
    user: dict = await repository.get_user(user_id=current_user.id)
    return Response(data=user)


@router.put("/user/", tags=["Users"], status_code=201)
async def update_user(request: Request, data: UserUpdateIncomeModel):
    current_user: CurrentUser = request.state.user
    repository: UserRepository = UserRepository()
    user: dict = await repository.get_user(user_id=current_user.id)
    await repository.update_user(user=user, data=data)
    await root.rabbit_manager.publish(Message(RabbitCall("/cacheuser", "PUT", {})))
    return Response(detail=_("Your info updated successfully"))
