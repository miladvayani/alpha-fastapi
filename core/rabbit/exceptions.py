from .responses import Status


class RabbitException(Exception):
    """Rabbit Base Exception"""

    status: Status
    detail: str

    def __init__(self, status: Status = 0, detail: str = "") -> None:
        self.status: Status = status
        self.detail: str = detail


class MethodNotAllowed(RabbitException):
    """Method Not Allowed"""

    status: Status = Status.reject
    detail: str = "Method Not Allowed"


class UrlNotFound(RabbitException):
    """Url not exists"""

    status: Status = Status.reject
    detail: str = "Url Not Found"


class MethodNotImplemented(RabbitException):
    """Method Not Implemented"""


class NotFound(RabbitException):
    """Not Found Error"""

    status: Status = Status.nack
    detail: str = "{condition} Not Found"

    def __init__(self, condition: str) -> None:
        self.detail = self.detail.format(condition)
