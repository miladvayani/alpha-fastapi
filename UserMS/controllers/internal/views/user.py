from typing import Union

from UserMS.controllers.internal.models.income.user import SetUserIncome
from UserMS.controllers.internal.models.outcome.user import SetUserOutcome

from UserMS.core.rabbit.exceptions import RabbitException
from .. import rabbit
from .. import api
from aio_pika import IncomingMessage
from UserMS.core.rabbit.responses import RabbitResponse as Response, Status
from UserMS.core.rabbit.request import RabbitRequest
from fastapi.responses import Response
from bson.objectid import ObjectId
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


@api.post("/user", response_model=SetUserOutcome)
async def set_user(user_info: SetUserIncome):
    repository = UserRepository()
    user: dict = await repository.set_user_by_mobile(
        mobile_number=user_info.mobile_number
    )
    return {"_id": user["_id"]}


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
