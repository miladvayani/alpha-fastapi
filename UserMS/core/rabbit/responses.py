from dataclasses import dataclass
from enum import Enum


class Status(int, Enum):
    """Rabbit Status Codes"""

    nack: 0
    ack: 1
    reject: 2


@dataclass
class RabbitResponse:
    """
    Rabbit Response
    """

    status: Status
    detail: str
    result: str
