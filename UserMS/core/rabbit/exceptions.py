from .responses import Status


class MethodNotAllowed(Exception):
    """Method not allowed"""


class UrlNotFound(Exception):
    """Url not exists"""


class MethodNotImplemented(Exception):
    """Method not implemented"""


class NotFound(Exception):
    """Not Found Error"""


class RabbitException(Exception):
    """Rabbit Base Exception"""

    status: Status
    detail: str

    def __init__(self, status: Status, detail: str) -> None:
        self.status: Status = status
        self.detail: str = detail
