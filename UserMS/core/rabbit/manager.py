import asyncio
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, List, Optional, Union
from aio_pika import Connection, Exchange
from aio_pika import Channel
from aio_pika import connect_robust
from aio_pika import Message
from aio_pika import Queue
from aio_pika import IncomingMessage

from .interface import PropertiesInterface, RabbitInterface
from .credentials import Credentials
from .handler import Handler
from .router import RabbitRouter
from .properties import HandlerProperties
from .properties import Properties


class RabbitManager(RabbitInterface):
    def __init__(
        self,
        connection_str: str,
        credentials: Credentials = None,
        handler_property: Union[HandlerProperties, dict] = {},
        declarations: List[Callable] = [],
    ) -> None:
        super().__init__(
            connection_str=connection_str,
            credentials=credentials,
            handler_property=handler_property,
            declarations=declarations,
        )
        self.router: RabbitRouter = RabbitRouter()
        self.__handler: Handler = (
            Handler(self.router)
            if not self.handler_property
            else Handler(self.router, **dict(self.handler_property))
        )

    async def create_connection(self, loop: asyncio.AbstractEventLoop = None):
        if loop is None:
            loop = asyncio.get_event_loop()
        if not self.credentials:
            self.connection = await connect_robust(self.connection_string, loop=loop)
        else:
            self.connection = await connect_robust(
                self.connection_string, **self.credentials.dict(), loop=loop
            )

    def declare(self, func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        self.declarations.append(func)
        return wrapper

    async def publish(
        self,
        message: Message,
        routing_key: str = None,
        correlation_id: Any = None,
        reply_to: str = None,
        expiration: Union[float, datetime, timedelta] = 1.1,
    ) -> bool:
        if routing_key is None:
            raise NotImplementedError("Routing Key Can not be null")
        channel = await self.connection.channel(publisher_confirms=False)
        is_published: bool = False
        async with channel.transaction():
            if expiration is not None:
                message.expiration = expiration
            if correlation_id:
                message.correlation_id = correlation_id
            if reply_to:
                message.reply_to = reply_to

            for declaration in self.declarations:
                result = await declaration(channel)
                if isinstance(result, Exchange):
                    exchange = result
                    await exchange.publish(message=message, routing_key=routing_key)
                    is_published = True
                    break
            if is_published is False:
                await channel.default_exchange.publish(
                    message,
                    routing_key=routing_key,
                )
        return is_published

    async def consume(
        self,
        queue: Queue,
        callback: Callable[[IncomingMessage], Any] = None,
        no_ack: bool = False,
        exclusive: bool = False,
        arguments: dict = None,
        consumer_tag: str = None,
        timeout: Optional[Union[int, float]] = None,
    ):
        await queue.consume(
            callback if callback else self.__handler.dispatch,
            no_ack,
            exclusive,
            arguments,
            consumer_tag,
            timeout,
        )
