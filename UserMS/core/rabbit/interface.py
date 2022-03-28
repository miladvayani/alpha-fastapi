from abc import ABC, abstractmethod
import asyncio
from datetime import datetime, timedelta
from typing import Any, Callable, Optional, Union

from aio_pika import Connection
from aio_pika import Channel
from aio_pika import Queue
from aio_pika import IncomingMessage
from aio_pika import Message

from .credentials import Credentials


class PropertiesInterface(ABC):
    @abstractmethod
    def dict(self) -> dict:
        ...


class RabbitInterface(ABC):
    def __init__(
        self,
        connection_str: str,
        credentials: Credentials = None,
        handler_property: Union[PropertiesInterface, dict] = {},
        declarations: list = [],
    ) -> None:
        """
        Rabbit Manager for handler requests, publish, connections and consumers.

        Args:
            connection_str (str): rabbit connection string
            credentials (Credentials, optional): security configs for rabbit robust connection.
            Defaults to None.
            handler_property (Union[PropertiesInterface, dict], optional): request handler properties.
            Defaults to {}.
            declarations (list[list[Callable, PropertiesInterface]], optional): list of pre defined
            delcrations such as `declare_queue` and `declare_exchange` methods for channel.
            Defaults to [].
        """
        self.connection_string = connection_str
        self.credentials: Credentials = credentials
        self.declarations: list = declarations
        self.handler_property: Union[PropertiesInterface, dict] = handler_property

    @abstractmethod
    async def create_connection(self, loop: asyncio.AbstractEventLoop = None) -> None:
        """create robust connection for rabbit

        Args:
            loop (asyncio.AbstractEventLoop, optional): current loop. Defaults to None.
        """
        ...

    @abstractmethod
    async def publish(
        self,
        message: Message,
        routing_key: str = None,
        correlation_id: Any = None,
        reply_to: str = None,
        expiration: Union[float, datetime, timedelta] = 1.1,
    ) -> bool:
        """publisher method.

        Args:
            message (Message): publish message
            routing_key (str, optional): routing key. Defaults to None.
            correlation_id (Any, optional): ... Defaults to None.
            reply_to (str, optional): ... Defaults to None.
            expiration (Union[float, datetime, timedelta], optional): ... Defaults to 1.1.
        Returns:
            bool: if published successfully will return True, otherwise False.
        """
        ...

    @abstractmethod
    def declare(self, func: Callable):
        """declare function for declaring queues, exhanges from external.
        all declared list invokes before publish and consumer.

        Args:
            func (Callable): channel instance will pass into decorated function.
        """

    @abstractmethod
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
        """consumer method.

        Args:
            queue (Queue): declared queue from outside.
            callback (Callable[[IncomingMessage], Any], optional): consumer callback, if
            it been `None` will use handler dispatcher as callback method. Defaults to None.
            no_ack (bool, optional): _description_. Defaults to False.
            exclusive (bool, optional): _description_. Defaults to False.
            arguments (dict, optional): _description_. Defaults to None.
            consumer_tag (str, optional): _description_. Defaults to None.
            timeout (Optional[Union[int, float]], optional): _description_. Defaults to None.
        """
