from asyncio import gather
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
    response_model=UserResponse,
)
async def get_user(request: Request):
    current_user: CurrentUser = request.state.user
    repository: UserRepository = UserRepository()
    user: dict = await repository.get_user(user_id=current_user.id)
    return Response(data=user)


@router.put("/user/", status_code=201)
async def update_user(request: Request, data: UserUpdateIncomeModel):
    current_user: CurrentUser = request.state.user
    repository: UserRepository = UserRepository()
    user: dict = await repository.get_user(user_id=current_user.id)
    print(data.last_name)
    await repository.update_user(user=user, data=data)
    await root.rabbit_manager.publish(
        Message(
            RabbitCall(
                url="/cacheuser",
                method="PUT",
                data=dict(
                    id=str(user["_id"]),
                    buyer_id=user["buyer_id"],
                    first_name=user["first_name"],
                    last_name=user["last_name"],
                ),
            ).jsonify()
        ),
        routing_key="auth_ms_test",
    )

    return Response(detail=_("Your info updated successfully"))
