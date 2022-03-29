from functools import wraps
from typing import Callable, List, NamedTuple
from aio_pika import IncomingMessage
from pydantic import BaseModel
from .responses import RabbitResponse as Response, Status
from .exceptions import MethodNotAllowed
from .exceptions import MethodNotImplemented
from .exceptions import UrlNotFound
from .exceptions import RabbitException
from .request import RabbitRequest as Request


class METHODS(NamedTuple):
    """Rabbit Methods

    Args:
        NamedTuple (tuple): methods.
    """

    POST: str = "POST"
    GET: str = "GET"
    PUT: str = "PUT"
    DELETE: str = "DELETE"


class RabbitRouter:
    def __init__(self) -> None:
        """ """
        self.__methods: METHODS = METHODS()
        self.routes: dict[str, list[dict[str, dict]]] = {
            "GET": [],
            "PUT": [],
            "DELETE": [],
            "POST": [],
        }

    def route(
        self, url: str, response_model: BaseModel = None, method: str = "GET"
    ) -> Callable:
        """register routes and add routes to router.
        whe

        Args:
            url (str): _description_
            response_model (BaseModel, optional): _description_. Defaults to None.
            method (str, optional): _description_. Defaults to "GET".

        Raises:
            MethodNotImplemented: _description_

        Returns:
            Callable: _description_
        """
        if method in self.__methods:

            def decorator(func: Callable) -> None:
                self.routes[method].append(
                    dict(
                        url=url, operate=dict(func=func, response_model=response_model)
                    )
                )

            return decorator
        else:
            raise MethodNotImplemented("Method not implemented")

    def find(self, method: str, url: str) -> Callable:
        if method in self.__methods:
            for route in self.routes[method]:
                if url == route["url"]:
                    return route["operate"]
            raise UrlNotFound("Url not exists")
        raise MethodNotAllowed("Method not allowed")

    async def call(
        self,
        func: Callable[[Request, IncomingMessage], Response],
        message: IncomingMessage,
        request: Request,
    ) -> Response:

        try:
            response: Response = await func(request, message=message)
            if response.status == Status.ack:
                message.ack()
            elif response.status == Status.nack:
                message.nack()
            elif response.status == Status.reject:
                message.reject()
        except RabbitException as err:
            if err.status == Status.nack:
                message.nack()
            else:
                message.reject(requeue=False)
            response.status = err.status
            response.detail = err.detail
        return response
