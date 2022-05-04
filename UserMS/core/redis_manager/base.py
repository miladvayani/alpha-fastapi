import aioredis
from typing import Union, Any
from abc import ABC, abstractmethod

class BaseRedis(ABC):
    """Interface for Redis.
    
    Attributes:
        connection (aioredis.Redis): Redis connection.
        address (str): Redis address.
        index (int): Redis database index.
        password (str): Redis password.
        ttl (int): Redis key expire time.
        pool (aioredis.ConnectionPool): Redis connection pool.
    

    Methods:
        set: Set value to Redis database.This method should be implemented in child class.
        get: Get value from Redis database.This method should be implemented in child class.
        delete: Delete key from Redis database
        update : Update value to Redis database if key exists.
        mget : Get multiple values from Redis database.

    """
    connection:aioredis.Redis = None
    address: str = None
    index:int = None
    password:str = None
    ttl: int = None
    pool:aioredis.ConnectionPool = None

    def __init__(self, address, password, index, ttl) -> None:
        BaseRedis.address = address
        BaseRedis.password = password
        BaseRedis.index = index
        BaseRedis.ttl = ttl

    @classmethod
    async def get_connection(cls)->aioredis.Redis:
        """Connect to Redis server.

        Returns:
            aioredis.Redis: Redis connection.
        """
        if not cls.connection:
            cls.pool = aioredis.ConnectionPool.from_url(
                url=cls.address + "/" + str(cls.index),
                decode_responses=True,
                password=cls.password,
            )
            cls.connection = aioredis.Redis(connection_pool=cls.pool)
        return cls.connection

    @abstractmethod
    async def set(self, key: Union[str, int], value: Any,ttl:int=None) -> None:
        """Set value to Redis database.

        Args:
            key (Union[str,int]):  key to set value to.
            value (Any): value to set.
            ttl (int): expire time in seconds.
        """

    @abstractmethod
    async def get(self, key: Union[str, int]) -> Any:
        """Get value from Redis database.

        Args:
            key (Union[str,int]): key to get value from.

        Returns:
            Any: value from Redis database.
        """
       

    @classmethod
    async def delete(cls, key: Union[str, int]) -> None:
        """Delete key from Redis database.

        Args:
            key (Union[str,int]): key to delete from Redis database.
        """
        await cls.connection.delete(key)

    @classmethod
    async def update(cls, key: Union[str, int], value: Any) -> None:
        """If key exists, update value.

        Args:
            key (Union[str,int]): key to update.
            value (Any): value to update.
        """
        if await cls.connection.exists(key):
            await cls.set(key, value)
        else:
            raise Exception("Key not found")

    @classmethod
    async def mget(cls, keys: list) -> list:
        """Get multiple values from Redis database.

        Args:
            keys (list): keys to get values from Redis database.

        Returns:
            list: values from Redis database.
        """
        result = []
        for item in keys:
            result.append(await cls.get(item))

        return result