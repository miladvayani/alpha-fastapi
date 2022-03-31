from dataclasses import dataclass
from enum import Enum
from typing import Any


class Status(int, Enum):
    """Rabbit Status Codes"""

    nack = 0
    ack = 1
    reject = 2
    unhandled = 3


@dataclass
class RabbitResponse:
    """
    Rabbit Response
    """

    status: Status = 1
    detail: str = ""
    result: Any = None
