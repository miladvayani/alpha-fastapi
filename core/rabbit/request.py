from typing import Callable
from urllib import parse


class RabbitRequest:
    def __init__(self) -> None:
        """Rabbit Request.

        Attributes:
            headers (dict): request headers
            query_params (dict): query params
            body (dict): request body
            url (str): request url
            method (str): request method
            client (tuple): request client
            view (Callable): view matched for reqeust
            content_type (str): request content_type
            host (str): request host address
            port (int): request port
            path (str): request path
        """
        self.headers: dict = {}
        self.query_params: dict = {}
        self.body: dict = {}
        self.url: str = None
        self.method: str = None
        self.client: tuple = tuple()
        self.view: Callable = None
        self.content_type: str = None
        self.host: str = None
        self.port: int = None
        self.path: str = None

    def create_request(self) -> None:
        """
        this method creates request infos.
        """
        parser = parse.urlsplit(self.url)
        self.query_params = dict(parse.parse_qsl(parser.query))
        self.host = parser.hostname
        self.port = parser.port
        self.client = (self.host, self.port)
        self.path = parser.path
