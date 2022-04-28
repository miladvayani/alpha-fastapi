from typing import final
from fastapi import Request
from .structors import LocalProxy
from .structors import LocalStack
from dataclasses import dataclass
from bson.objectid import ObjectId


@final
class Messages(LocalStack):
    pass


@final
class Requests(LocalStack):
    pass


@dataclass
class CurrentUser:

    _id: str = None
    workspace: ObjectId = None
    pos_id: str = None
    mobile_number: str = None
    first_name: str = None
    last_name: str = None
    buyer_id: str = None
    title: str = None
    is_owner: bool = None
    id: ObjectId = None
    client_id: ObjectId = None
    is_authenticated: bool = False
    is_anonymous: bool = True


message_context = Messages()
request_context = Requests()

message: LocalProxy = LocalProxy[Messages](
    message_context, context=False, stackable=True
)
request: Request = LocalProxy[Request](request_context, context=True, stackable=False)
