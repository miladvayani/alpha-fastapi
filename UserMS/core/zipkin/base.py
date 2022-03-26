from functools import wraps
from fastapi import Request
from typing import Any, Callable, List, Optional
from aiozipkin import SpanAbc, create
from aiozipkin import Tracer
from asyncio import AbstractEventLoop
from .properties import ZipkinEndpoint
from .properties import ZipkinTracerConfig
from .properties import KINDS


class ZipkinManager:
    """
    Zipkin manager for `aiozipkin` driver.
    """

    def __init__(self, configs: ZipkinTracerConfig) -> None:
        """

        Args:
            configs (ZipkinTracerConfig): needed configs for zipkin manager class.

        Attributes:
            __handlers (List[Callable]): list of handlers for monitoring using
            `ZipkinManager.handler` decorator method.
            __trace__ (Tracer): Trace instance
            root_span (SpanAbc): root span for each trace after connection and instrumentations.

        """
        self.configs: ZipkinTracerConfig = configs
        self.__handlers: List[Callable] = []
        self.__trace__: Tracer = None
        self.root_span: SpanAbc = None

    def handler(
        self,
        _func: Optional[Callable] = None,
        *,
        sampled: Optional[bool] = None,
        debug: bool = False,
        tag: dict = {"span_type", "root"},
        kind: str = KINDS.CLIENT,
        start_annotate: str = None,
        end_annotate: str = None,
    ) -> Tracer:
        """this method is a decorator for creating an instrumentation to zipkin.

        Args:
            _func (Optional[Callable], optional): function to decorate. Defaults to None.
            sampled (Optional[bool], optional): Defaults to None.
            debug (bool, optional): trace debug mode. Defaults to False.
            tag (dict, optional): trace tag name. Defaults to {"span_type", "root"}.
            kind (str, optional): trace destination that modify sender and reciever kind.
            Defaults to KINDS.CLIENT.
            start_annotate (str, optional): trace start annotation. Defaults to None.
            end_annotate (str, optional): trace end annotation. Defaults to None.

        Returns:
            Callpable: decorated handler
        """
        start_annotate = start_annotate
        end_annotate = end_annotate

        def dec(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                request: Request = kwargs.get("request", None) or args[0]
                if start_annotate is None:
                    start_annotate = "START [REQUEST] : " + request.full_url
                if end_annotate is None:
                    end_annotate = "END [REQUEST] : " + request.full_url
                tracer = await self.trace()
                self.monitor(
                    tracer,
                    func,
                    sampled=sampled,
                    debug=debug,
                    tag=tag,
                    kind=kind,
                    start_annotate=start_annotate,
                    end_annotate=end_annotate,
                    *args,
                    **kwargs,
                )

            return wrapper

        if _func is None:
            return dec
        decorated = dec(_func)
        self.__handlers.append(decorated)
        return decorated

    async def monitor(
        self,
        tracer: Tracer,
        handler: Callable,
        sampled: Optional[bool],
        debug: bool,
        tag: dict,
        kind: str,
        start_annotate: str,
        end_annotate: str,
        *args: tuple,
        **kwargs: dict,
    ) -> Any:
        """monitor the handler that will trace using zipkin.

        Args:
            tracer (Tracer): `Tracer` instance.
            handler (Callable): handler to monitor.
            sampled (Optional[bool]):
            debug (bool): trace debug mode.
            tag (dict): trace tag name.
            kind (str): trace destination that modify sender and reciever kind.
            start_annotate (str): trace start annotation. Defaults to None.
            end_annotate (str): trace end annotation. Defaults to None.

        Returns:
            Any: handler result after tracing.
        """
        with tracer.new_trace(sampled=sampled, debug=debug) as span:
            span.name(handler.__name__)
            span.tag(*tuple(tag))
            span.kind(kind)
            span.annotate(start_annotate)
            result = await handler(*args, **kwargs)
            span.annotate(end_annotate)
            return result

    async def trace(
        self, loop: AbstractEventLoop = None, new_endpoint: ZipkinEndpoint = None
    ) -> Tracer:
        """create a new trace connection

        Args:
            loop (AbstractEventLoop, optional): current loop. Defaults to None.
            new_endpoint (ZipkinEndpoint, optional): local zipkin endpoint that demonstrate instrumentation starter.
            if new_endpoint been empty/None will use declared endpoint from config.
            Defaults to None.

        Returns:
            Tracer: created trace instance.
        """
        self.__trace__ = await create(
            zipkin_address=self.configs.zipkin_address,
            local_endpoint=self.configs.local_endpoint
            if not new_endpoint
            else new_endpoint,
            sample_rate=self.configs.sample_rate,
            send_interval=self.configs.send_interval,
            loop=self.configs.loop if not loop else loop,
            ignored_exceptions=self.configs.ignored_exceptions,
        )
        return self.__trace__

    @property
    def get_trace(self) -> Tracer:
        return self.__trace__
