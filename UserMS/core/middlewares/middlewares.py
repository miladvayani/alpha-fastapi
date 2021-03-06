import ast
from base64 import b64decode
from typing import List, Union
import json
from types import SimpleNamespace
from typing import Callable, Optional
from typing import Any
from fastapi import Request
from fastapi import HTTPException
from bson.objectid import ObjectId
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.middleware.base import DispatchFunction
from starlette.types import ASGIApp

from ..proxies.structors import LocalProxy
from ..responses import Response

from ..zipkin import ZipkinManager
from ..zipkin import KINDS
from ..jwt import JWTManager
from ..aes import AES
from ..proxies import message
from ..proxies import CurrentUser
from ..i18n import Babel


class ProxyMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        proxies: List[LocalProxy] = [],
        lookupers: List[Callable[[Request], Any]] = [],
        dispatch: DispatchFunction = None,
    ) -> None:
        """_summary_

        Args:
            app (ASGIApp): ...
            proxies (list[LocalProxy], optional): list of proxies. Defaults to [].
            lookupers (list[Callable[[Request], Any]], optional): list of lookupers
            for proxies. Defaults to [].
            dispatch (DispatchFunction, optional): dispatch function.
            Defaults to None.
        """
        super().__init__(app, dispatch)
        self.proxies: list[LocalProxy] = proxies
        self.lookupers: list[Callable[[Request], Any]] = lookupers

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """dispatch function

        Args:
            request (Request): ...
            call_next (RequestResponseEndpoint): ...

        Returns:
            Response: ...
        """
        for idx, proxy in enumerate(self.proxies):
            lookup = None
            if idx in self.lookupers:
                lookup = self.lookupers[idx](request)
            proxy.start(request, lookup=lookup)
        response = await call_next(request)
        return response


class ZipkinMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        manager: ZipkinManager,
        configs: dict,
        dispatch: DispatchFunction = None,
    ) -> None:
        """_summary_

        Args:
            app (ASGIApp): ...
            manager (ZipkinManager): instance
            configs (dict): needed configs
            dispatch (DispatchFunction, optional): dispatch function.
            Defaults to None.
        """
        super().__init__(app, dispatch)
        self.manager: ZipkinManager = manager
        self.sampled: Optional[bool] = configs.get("ZIPKIN_SAMPLED", None)
        self.debug: bool = configs.get("DEBUG" or "debug", False)
        self.tag: dict = configs.get("ZIPKIN_TAG", ("span_type", "root"))
        self.kind: str = configs.get("ZIPKIN_KIND", KINDS.CLIENT)
        self.start_annotate: str = configs.get("ZIPKIN_START_ANNOTATE", None)
        self.end_annotate: str = configs.get("ZIPKIN_END_ANNOTATE", None)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """dispatch function

        Args:
            request (Request): ...
            call_next (RequestResponseEndpoint): ...

        Returns:
            Response: ...
        """
        host, port = request.scope["server"]
        scheme = request.scope["scheme"]
        path = request.scope["path"]
        client_process_id = request.scope["client"][1]
        if self.start_annotate is None:
            self.start_annotate = f"START || CLIENT[{client_process_id}] [REQUEST::{request.method}] == {scheme}://{host}:{port}{path}"
        if self.end_annotate is None:
            self.end_annotate = f"END || CLIENT[{client_process_id}] [REQUEST::{request.method}] == {scheme}://{host}:{port}{path}"
        tracer = await self.manager.trace()
        with tracer.new_trace(sampled=self.sampled, debug=self.debug) as span:
            span.name(f"{scheme}://{host}:{port}{path}")
            span.tag(*tuple(self.tag))
            span.kind(self.kind)
            span.annotate(self.start_annotate)
            self.manager.root_span = span
            response = await call_next(request)
            span.annotate(self.end_annotate)
        await tracer.close()
        return response


class AuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        manager: JWTManager,
        configs: dict,
        dispatch: DispatchFunction = None,
    ) -> None:
        """_summary_

        Args:
            app (ASGIApp): ...
            manager (JWTManager): instance
            configs (dict): needed configs
            redis (Redis): ...
            dispatch (DispatchFunction, optional): dispatch function.
            Defaults to None.
        """
        super().__init__(app, dispatch)
        self.configs: dict = configs
        self.manager: JWTManager = manager

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """dispatch function

        Args:
            request (Request): ...
            call_next (RequestResponseEndpoint): ...

        Returns:
            Response: ...
        """
        token: str = request.headers.get("Authorization", None)
        request.state.user = CurrentUser()
        if token:
            try:
                user = self.get_data(token)
                request.state.user = user
            except HTTPException as error:
                message(error.detail)
                return Response(status_code=error.status_code)
            except Exception:
                message("Invalid Token")
                return Response(status_code=401)
        response = await call_next(request)
        return response

    def get_data(self, token: str) -> Union[CurrentUser, None]:
        """
        Decrypt token and return data
        """
        token = token.strip()
        token = token.split(" ")[-1]
        jwt_token = token
        payload = self.manager.decode(
            jwt_token,
        )
        data = b64decode(payload["data"])
        iv = b64decode(payload["identifier"])
        dt = AES(self.configs.get("AES_KEY")).decrypt_ctr(data, iv)
        dt = dt.replace("'", '"').replace("None", "null")
        user: CurrentUser = json.loads(dt, object_hook=lambda e: CurrentUser(**e))
        user.is_authenticated = True
        user.id = user._id
        return user


class InternationalizationMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app: ASGIApp, babel: Babel, dispatch: DispatchFunction = None
    ) -> None:
        super().__init__(app, dispatch)
        self.babel: Babel = babel

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """dispatch function

        Args:
            request (Request): ...
            call_next (RequestResponseEndpoint): ...

        Returns:
            Response: ...
        """
        lang_code: str = request.headers.get("Accept-Language", "fa")
        self.babel.locale = lang_code
        response = await call_next(request)
        return response
