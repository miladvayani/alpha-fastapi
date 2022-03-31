from aio_pika import Channel
from fastapi import FastAPI
from pydantic import BaseSettings
from pymongo import MongoClient
from pymongo.database import Database

from .core.contrib import Mongo
from .core.contrib import Redis
from .core.contrib import babel
from .core.contrib import cli
from .core.contrib import RabbitManager
from .core.contrib import JWTManager
from .core.contrib import message
from .core.contrib import request
from .core.contrib import Response
from .core.contrib import ZipkinManager
from .core.contrib import BaseResponse
from .core.contrib import ZipkinTracerConfig
from .core.contrib import ZipkinEndpoint
from .core.contrib import CurrentUser
from .core.contrib import RabbitManager


class Application:

    app: FastAPI = ...
    client: MongoClient = ...
    db: Database = ...
    config: dict = ...
    jwt: JWTManager = ...
    zipkin: ZipkinManager = ...
    rabbit_manager: RabbitManager = ...
    redis: Redis = ...


def create_app(config: BaseSettings) -> FastAPI:
    root = Application

    # Install Configurations
    root.config = config.dict()

    root.config["CONNECTION_STRING"] = (
        root.config["MONGO_CONNECTION"]
        + root.config["MONGO_DB"]
        + root.config["MONGO_OPTIONS"]
    )
    root.config["AES_KEY"] = bytes(root.config["AES_KEY"].encode("utf-8"))
    root.config["JWT_PUBLIC"] = (
        root.config.get("JWT_PUBLIC").replace("\\n", "\n").strip().replace('"', "")
    )
    # Install Asgi Framework
    root.app = FastAPI(
        debug=root.config.get("DEBUG", False),
        title="Authentication Service",
        default_response_class=BaseResponse,
    )

    # Install Middlewares---------------------------------------------------------------
    from fastapi.middleware.cors import CORSMiddleware
    from .core.middlewares import ProxyMiddleware
    from .core.middlewares import AuthorizationMiddleware
    from .core.middlewares import InternationalizationMiddleware
    from .core.middlewares import ZipkinMiddleware

    root.zipkin = ZipkinManager(
        configs=ZipkinTracerConfig(
            zipkin_address=root.config["ZIPKIN_ADDRESS"],
            local_endpoint=ZipkinEndpoint(
                serviceName=root.config.get("ZIPKIN_SERVICE_NAME"),
                ipv4="127.0.0.1",
                port=8080,
                ipv6=None,
            ),
        )
    )
    root.redis = Redis(root.config)
    root.jwt = JWTManager(
        algorithm=root.config["JWT_ALGORITHM"],
        key=root.config["JWT_PUBLIC"],
        verify=True,
        options={},
    )
    root.app.add_middleware(
        CORSMiddleware,
        allow_origins=root.config.get("ALLOWED_HOSTS", "*"),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    root.app.add_middleware(
        AuthorizationMiddleware, manager=root.jwt, configs=root.config, redis=root.redis
    )
    root.app.add_middleware(
        ProxyMiddleware,
        proxies=[request, message],
        lookupers=[lambda request: request],
    )
    root.app.add_middleware(InternationalizationMiddleware, babel=babel)
    root.app.add_middleware(ZipkinMiddleware, manager=root.zipkin, configs=root.config)

    # Install Exceptions---------------------------------------------------------------

    from .core.exceptions import base_exception_handler
    from .core.exceptions import http_422_error_handler
    from .core.exceptions import http_duplicate_error_handler
    from .core.exceptions import http_500_error_handler
    from .core.exceptions import rabbit_mongodb_connection_error_handler
    from .core.exceptions import rabbit_duplicate_error_handler
    from .core.exceptions import DuplicateKeyError
    from .core.exceptions import HTTPException
    from .core.exceptions import ConnectionFailure
    from fastapi.exceptions import RequestValidationError
    from starlette.exceptions import HTTPException as StarletteHTTPException

    root.app.add_exception_handler(HTTPException, base_exception_handler)
    root.app.add_exception_handler(StarletteHTTPException, base_exception_handler)
    root.app.add_exception_handler(RequestValidationError, http_422_error_handler)
    root.app.add_exception_handler(DuplicateKeyError, http_duplicate_error_handler)
    root.app.add_exception_handler(Exception, http_500_error_handler)

    # Install Plugins
    root.rabbit_manager = RabbitManager(root.config["BROKER_URL"])
    root.rabbit_manager.add_exception_hanlder(
        ConnectionFailure, rabbit_mongodb_connection_error_handler
    )
    root.rabbit_manager.add_exception_hanlder(
        DuplicateKeyError, rabbit_duplicate_error_handler
    )

    @root.rabbit_manager.declare
    async def declare(channel: Channel):
        await channel.declare_queue("auth_ms_test", durable=True)

    # # Install Event Handlers
    # # Install Application connections
    # # Startup Factory ------------------------------------------------------------------
    @root.app.on_event("startup")
    async def startup():
        await Mongo(root.config).create_connection()
        connection = await root.rabbit_manager.create_connection()
        channel = await connection.channel()
        # queue = await channel.declare_queue(
        #     root.config["QUEUE_NAME"], durable=True, auto_delete=True
        # )
        queue = await channel.declare_queue("user_ms_test", durable=True)
        await root.rabbit_manager.consume(queue=queue)
        root.db = Mongo.db
        root.client = Mongo.client

    # Install Applications
    from .controllers.external import router
    from .controllers.internal import api

    root.app.include_router(router)
    root.app.include_router(api)

    return root.app
