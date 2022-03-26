from pydantic import BaseSettings


class Development(BaseSettings):

    DEBUG: bool = False
    ZIPKIN_ADDRESS: str
    ZIPKIN_SAMPLED: bool = True
    ZIPKIN_TAG: tuple = ("span_type", "root")
    ZIPKIN_KIND: str
    ZIPKIN_START_ANNOTATE: str = None
    ZIPKIN_END_ANNOTATE: str = None
    ZIPKIN_SERVICE_NAME: str
    MEMORY_MIN: int
    SECRET_KEY: str
    ALLOWED_HOSTS: str
    AES_KEY: str
    JWT_PUBLIC: str
    JWT_ALGORITHM: str
    APM_SERVER_URL: str
    APM_ENVIRONMENT: str
    APM_DEBUG: int
    APM_LOG_LEVEL: str
    BROKER_URL: str
    MONGO_CONNECTION: str
    MONGO_OPTIONS: str
    MONGO_DB: str
    QUEUE_NAME: str
    AUTH_QUEUE_NAME: str
    CONSTANTS_MS_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
