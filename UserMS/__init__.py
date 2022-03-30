from aio_pika import Channel
from fastapi import FastAPI
from pydantic import BaseSettings
from pymongo import MongoClient
from pymongo.database import Database

from .core import contrib


class Application:

    app: FastAPI = ...
    client: MongoClient = ...
    db: Database = ...
    config: dict = ...
    jwt: contrib.jwt.JWTManager = ...
    zipkin: contrib.zipkin.ZipkinManager = ...
    rabbit_manager: contrib.rabbit.RabbitManager = ...
    redis: contrib.redis.Redis = ...


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
        default_response_class=contrib.response.BaseResponse,
    )

    # Install Middlewares---------------------------------------------------------------
    from fastapi.middleware.cors import CORSMiddleware
    from .core.middlewares import ProxyMiddleware
    from .core.middlewares import AuthorizationMiddleware
    from .core.middlewares import InternationalizationMiddleware
    from .core.middlewares import ZipkinMiddleware

    root.zipkin = contrib.zipkin.ZipkinManager(
        configs=contrib.zipkin.ZipkinTracerConfig(
            zipkin_address=root.config["ZIPKIN_ADDRESS"],
            local_endpoint=contrib.zipkin.ZipkinEndpoint(
                serviceName=root.config.get("ZIPKIN_SERVICE_NAME"),
                ipv4="127.0.0.1",
                port=8080,
                ipv6=None,
            ),
        )
    )
    root.redis = contrib.redis.Redis(root.config)
    root.jwt = contrib.jwt.JWTManager(
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
        proxies=[contrib.proxies.request, contrib.proxies.message],
        lookupers=[lambda request: request],
    )
    root.app.add_middleware(InternationalizationMiddleware, babel=contrib.i18n.babel)
    root.app.add_middleware(ZipkinMiddleware, manager=root.zipkin, configs=root.config)

    # Install Exceptions---------------------------------------------------------------

    from .core.exceptions import base_exception_handler
    from .core.exceptions import http_422_error_handler
    from .core.exceptions import http_duplicate_error_handler
    from .core.exceptions import http_500_error_handler
    from .core.exceptions import DuplicateKeyError
    from .core.exceptions import HTTPException
    from fastapi.exceptions import RequestValidationError
    from starlette.exceptions import HTTPException as StarletteHTTPException

    root.app.add_exception_handler(HTTPException, base_exception_handler)
    root.app.add_exception_handler(StarletteHTTPException, base_exception_handler)
    root.app.add_exception_handler(RequestValidationError, http_422_error_handler)
    root.app.add_exception_handler(DuplicateKeyError, http_duplicate_error_handler)
    root.app.add_exception_handler(Exception, http_500_error_handler)

    # Install Plugins
    root.rabbit_manager = contrib.rabbit.RabbitManager(root.config["BROKER_URL"])

    @root.rabbit_manager.declare
    async def declare(channel: Channel):
        await channel.declare_queue("auth_ms_test", durable=True)

    # # Install Event Handlers
    # # Install Application connections
    # # Startup Factory ------------------------------------------------------------------
    @root.app.on_event("startup")
    async def startup():
        await contrib.mongo.Mongo(root.config).create_connection()
        connection = await root.rabbit_manager.create_connection()
        channel = await connection.channel()
        queue = await channel.declare_queue(
            root.config["QUEUE_NAME"], durable=True, auto_delete=True
        )
        await root.rabbit_manager.consume(queue=queue)
        root.db = contrib.mongo.Mongo.db
        root.client = contrib.mongo.Mongo.client

    # Install Applications
    from .controllers.external import router
    from .controllers.internal import api

    root.app.include_router(router)
    root.app.include_router(api)

    return root.app
