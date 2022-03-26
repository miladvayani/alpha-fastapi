from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Optional, Union
import json as JsonType
from .interface import PropertiesInterface


class Properties(PropertiesInterface):
    def dict(self):
        return self.__dict__


@dataclass
class RabbitCall(Properties):

    url: str
    method: str
    data: Any

    def jsonify(self, jsonifier: JsonType = JsonType, encode: bool = True) -> str:
        result = jsonifier.dumps(self.__dict__)
        if encode:
            return result.encode("utf-8")
        return result


@dataclass
class HandlerProperties(Properties):

    requeue: bool = False
    reject_on_redelivered: bool = False
    ignore_processed: bool = True


@dataclass
class QueueDeclarationProperties(Properties):
    """queue declration parameters. this will use in pre-defined declrations.

    Args:
        name (str): queue name. Defaults to None.
        durable (bool): _description_. Defaults to None.
        exclusive (bool): _description_. Defaults to None.
        passive (bool): _description_. Defaults to None.
        auto_delete (bool): _description_. Defaults to None.
        timeout (int): _description_. Defaults to None.
    """

    name: str = None
    durable: bool = False
    exclusive: bool = False
    passive: bool = False
    auto_delete: bool = False
    arguments: dict = None
    timeout: int = None


@unique
class ExchangePropertiey(str, Enum):
    FANOUT = "fanout"
    DIRECT = "direct"
    TOPIC = "topic"
    HEADERS = "headers"
    X_DELAYED_MESSAGE = "x-delayed-message"
    X_CONSISTENT_HASH = "x-consistent-hash"
    X_MODULUS_HASH = "x-modulus-hash"


@dataclass
class ExchangeDeclarationProperties(Properties):
    name: str
    type: Union[ExchangePropertiey, str] = ExchangePropertiey.DIRECT
    durable: bool = False
    auto_delete: bool = False
    internal: bool = False
    passive: bool = False
    arguments: dict = None
    timeout: Optional[Union[int, float]] = None
