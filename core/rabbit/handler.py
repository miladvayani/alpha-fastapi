from inspect import iscoroutinefunction
from typing import Callable, Dict
from aio_pika import IncomingMessage
from json import loads

from orjson import dumps
from pydantic import BaseModel

from .exceptions import RabbitException
from .exceptions import MethodNotAllowed
from .exceptions import UrlNotFound
from .exceptions import NotFound
from .router import RabbitRouter
from .responses import RabbitResponse as Response, Status
from .request import RabbitRequest as Request


class Handler:
    def __init__(
        self,
        router: RabbitRouter,
        requeue: bool = False,
        reject_on_redelivered: bool = False,
        ignore_processed: bool = True,
    ) -> None:
        """Handler is callback manager and request dispatcher for
        rabbit income messages.

        handler uses a router to handler request's and views for
        callback of consumer.

        this reduces concerns around the related tasks for consumer callback.

        Args:
            router (RabbitRouter): instance of `RabbitRouter`
            requeue (bool, optional): if requeue been False will reject unacked message
            but else, will put back it in queue again. Defaults to False.
            reject_on_redelivered (bool, optional): reject if delivered after first time.
            Defaults to False.
            ignore_processed (bool, optional): ignores already processed messages. Defaults to True.
        """
        self.router: RabbitRouter = router
        self.message: IncomingMessage = None
        self.requeue: bool = requeue
        self.reject_on_redelivered: bool = reject_on_redelivered
        self.ignore_processed: bool = ignore_processed
        self.exception_handlers: Dict[Exception, Callable] = {}
        self.json_decoder = loads
        self.json_encoder = dumps

    async def dispatch(
        self,
        message: IncomingMessage,
    ) -> Response:
        """dispatch incoming messages and this should register as a cosumer callback.

        Args:
            message (IncomingMessage): ...

        Returns:
            Response: `RabbitResponse` message.
        """
        async with message.process(
            requeue=self.requeue,
            reject_on_redelivered=self.reject_on_redelivered,
            ignore_processed=self.ignore_processed,
        ):
            request: Request = Request()
            body: dict = self.deserialize(message.body.decode("utf-8"))
            print(body)
            request.body = body["data"]
            request.url = body["url"]
            request.method = body["method"]
            request.content_type = message.content_type
            request.headers = message.headers
            request.create_request()
            response: Response = await self.make_response(
                view=request.view, message=message, request=request
            )
            if response.status == 3:
                response.status = 0
                error = response.result.pop("error")
                response.result = None
                print(response)
                raise error
            print(response)
        self.message = None

    def deserialize(self, content: str) -> dict:
        """deserialize income message body.

        Args:
            content (str): body

        Returns:
            dict: ...
        """
        return self.json_decoder(content)

    def serialize(self, data: dict) -> str:
        """serialize income message body.

        Args:
            data (dict): body

        Returns:
            str: ...
        """
        return self.json_encoder(data)

    def add_exception_handler(self, exception: Exception, handler: Callable) -> None:
        self.exception_handlers[exception] = handler

    async def make_response(
        self,
        view: dict[dict[str, Callable], dict[str, BaseModel]],
        request: Request,
        message: IncomingMessage,
    ) -> Response:
        try:
            route: dict[dict[str, Callable], dict[str, BaseModel]] = self.router.find(
                url=request.path, method=request.method
            )
            view = request.view = route["func"]
            response = await self.router.call(view, message, request)
            if response is not None:
                if response.status == Status.ack:
                    await message.ack()
                elif response.status == Status.nack:
                    await message.nack(requeue=False)
                elif response.status == Status.reject:
                    await message.reject(requeue=False)
            else:
                response = Response()
            return response
        except (RabbitException, MethodNotAllowed, UrlNotFound, NotFound) as err:
            if err.status == Status.nack:
                await message.nack(requeue=False)
            else:
                await message.reject(requeue=False)
            response.status = err.status
            response.detail = err.detail
            return response
        except Exception as exp:
            if type(exp) in self.exception_handlers:
                exception_handler = self.exception_handlers[type(exp)]
                if iscoroutinefunction(exception_handler):
                    response = await exception_handler(message, exp)
                else:
                    response = exception_handler(message, exp)
            response.status = 3
            response.detail = "Internal Server Error"
            response.result = {"error": exp}
            return response
