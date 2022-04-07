from typing import Union
from fastapi.responses import Response
from aio_pika import IncomingMessage
from bson.objectid import ObjectId
from .. import rabbit
from .. import api

from UserMS.core.contrib import RabbitResponse as Response, Status
from UserMS.core.contrib import RabbitRequest
from UserMS.core.contrib import RabbitException

from ..models.income.user import SetUserIncome
from ..models.outcome.user import SetUserOutcome
from ..logic.user import UserRepository


@rabbit.route("/user")
async def get_user(request: RabbitRequest, message: IncomingMessage) -> Response:
    _id: Union[ObjectId, None] = request.body.get("_id", None)
    repository = UserRepository()
    if _id:
        result = await repository.get_user_by_id(user_id=_id)
    else:
        result = await repository.get_users(request.body)
    return result


@api.post("/user")
async def set_user(user_info: SetUserIncome):
    repository = UserRepository()
    user_id: dict = await repository.set_user_by_mobile(
        mobile_number=user_info.mobile_number
    )
    print(user_id)
    return {"_id": str(user_id)}


@rabbit.route("/user/one", method="PUT")
async def update_one_user(request: RabbitRequest, message: IncomingMessage) -> Response:
    _id: str = request.body.get("_id", None)
    repository = UserRepository()
    if repository.update_one_user(user_id=_id, new_data=request.body["document"]):
        return Response(
            result=True, status=Status.ack, detail=f"{_id} User updated successfully"
        )
    raise RabbitException(Status.reject, "User collection has not any changed!")


@rabbit.route("/user/many", method="PUT")
async def update_many_user(
    request: RabbitRequest, message: IncomingMessage
) -> Response:
    repository = UserRepository()
    updated_count = await repository.update_bulk_user(
        query=request.body["query"], new_data=request.body["document"]
    )
    if updated_count:
        return Response(
            result=True,
            status=Status.ack,
            detail=f"{updated_count} User updated successfully",
        )
    raise RabbitException(Status.reject, "User collection has not any changed!")
