# try:

from .jwt import JWTManager
from .jwt import token_required

from .hydantic import fields
from .hydantic import validators
from .hydantic import options

from .exceptions import base_exception_handler
from .exceptions import http_422_error_handler
from .exceptions import http_500_error_handler
from .exceptions import http_duplicate_error_handler
from .exceptions import DuplicateKeyError

from .i18n import babel
from .i18n import _
from .i18n import cli

from .middlewares import AuthorizationMiddleware
from .middlewares import BaseHTTPMiddleware
from .middlewares import ProxyMiddleware
from .middlewares import InternationalizationMiddleware

from .mongo import Mongo

from .permissions.checker import PermissionChecker
from .permissions.services import UserAuthenticated
from .permissions.services import WorkspaceOwner
from .permissions.services import WorkspaceUser

from .rabbit.manager import RabbitManager
from .rabbit.exceptions import RabbitException
from .rabbit.properties import HandlerProperties
from .rabbit.properties import RabbitCall
from .rabbit.properties import ExchangePropertiey
from .rabbit.request import RabbitRequest
from .rabbit.responses import RabbitResponse
from .rabbit.responses import Status

from .redis import Redis

from .responses import Response as BaseResponse
from .responses import ResponseObject as Response

from .zipkin import ZipkinManager
from .zipkin import ZipkinTracerConfig
from .zipkin import ZipkinEndpoint
from .zipkin import KINDS

from .proxies import request
from .proxies import message

from .proxies import CurrentUser

# except ImportError as err:
#     from subprocess import run
#     from platform import python_version

#     pv = python_version().split(".")
#     PY: int = float(pv[0] + "." + pv[1])
#     if PY > 3.7:
#         run(["pip", "install", f"{err.name}"])
#     else:
#         raise SystemError("Please upgrade your python to version 3.7+")
