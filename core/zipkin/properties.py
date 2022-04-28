from asyncio import AbstractEventLoop
from typing import List, NamedTuple, Optional, Type
from aiozipkin import SERVER
from aiozipkin import PRODUCER
from aiozipkin import CLIENT
from aiozipkin import CONSUMER
from aiozipkin.helpers import Endpoint


class ZipkinEndpoint(Endpoint):
    """Zipkin Endpoint Parameters.


    Args:
        serviceName (str, optional): zipkin service name.
        ipv4 (str, optional): localhost or sender ip based on ipv4
        ipv6 (str, optional): localhost or sender ip based on ipv6
        port (str, optional): localhost or sender port
    """

    pass


class ZipkinTracerConfig(NamedTuple):
    """`ZipkinTracer` instance configs/parameters.

    Args:
        zipkin_address (str): zipkin address
        local_endpoint (ZipkinEndpoint): endpoint instance
        sample_rate (float): ..., Default is 0.01
        send_interval (float): ..., Default is 5
        loop (AbstractEventLoop): ..., Default is None
        ignored_exceptions (Optional[List[Type[Exception]]]): ..., Default is None
    """

    zipkin_address: str
    local_endpoint: Endpoint
    sample_rate: float = 0.01
    send_interval: float = 5
    loop: AbstractEventLoop = None
    ignored_exceptions: Optional[List[Type[Exception]]] = None


class KINDS:
    SERVER = SERVER
    PRODUCER = PRODUCER
    CLIENT = CLIENT
    CONSUMER = CONSUMER
