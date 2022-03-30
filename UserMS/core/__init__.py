class contrib:
    try:

        class jwt:
            from .jwt import JWTManager
            from .jwt import token_required

        class exceptions:
            from .exceptions import base_exception_handler
            from .exceptions import http_422_error_handler
            from .exceptions import http_500_error_handler
            from .exceptions import http_duplicate_error_handler
            from .exceptions import DuplicateKeyError

        class i18n:
            from .i18n import babel
            from .i18n import _

        class middlewares:
            from .middlewares import AuthorizationMiddleware
            from .middlewares import BaseHTTPMiddleware
            from .middlewares import ProxyMiddleware
            from .middlewares import InternationalizationMiddleware

        class mongo:
            from .mongo import Mongo

        class permissions:
            from .permissions.checker import PermissionChecker
            from .permissions.services import UserAuthenticated
            from .permissions.services import WorkspaceOwner
            from .permissions.services import WorkspaceUser

        class rabbit:
            from .rabbit.manager import RabbitManager
            from .rabbit.exceptions import RabbitException
            from .rabbit.properties import HandlerProperties
            from .rabbit.properties import RabbitCall
            from .rabbit.properties import ExchangePropertiey
            from .rabbit.request import RabbitRequest
            from .rabbit.responses import RabbitResponse
            from .rabbit.responses import Status

        class redis:
            from .redis import Redis

        class response:
            from .responses import Response as BaseResponse
            from .responses import ResponseObject as Response

        class zipkin:
            from .zipkin import ZipkinManager
            from .zipkin import ZipkinTracerConfig
            from .zipkin import ZipkinEndpoint
            from .zipkin import KINDS

        class proxies:
            from .proxies import request
            from .proxies import message

    except ImportError as err:
        from subprocess import run
        from platform import python_version

        PY: int = float(python_version())
        if PY > 3.7:
            run([f"pip", "install", "{err.name}"])
        else:
            raise SystemError("Please upgrade your python to version 3.7+")
